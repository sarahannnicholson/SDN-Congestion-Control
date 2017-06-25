from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER, DEAD_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from math import ceil
from ryu.lib import hub
from ryu import cfg
import subprocess

CONF = cfg.CONF

class NetworkMonitor(app_manager.RyuApp):

    def __init__(self, *args, **kwargs):
        super(NetworkMonitor, self).__init__(*args, **kwargs)
        # Bandwith threshold in Kbit/s
        self.bw_threshold = 5000
        self.bw_min = 100
        self.datapaths = {}
        self.query_interval = 2
        self.port_speed = {}
        self.flow_speed = {}
        self.state_len = 3
        self.flow_byte_counts = {}
        self.monitor_thread = hub.spawn(self._monitor)
        self.rate_limited_switches = []
        self.switch_interfaces = ["s1-eth3", "s2-eth1"]
        self.dpids = {0x1: "s1", 0x2: "s2"}

    def apply_rate_limiting(self, switch, in_port, out_port, rate):
        c_rate = int(ceil(rate))
        switch_id = switch + "-eth" + str(in_port) + str(out_port)
        ingressPolicingBurst, ingressPolicingRate = "ingress_policing_burst=10", "ingress_policing_rate=5000"
        if not switch_id in self.rate_limited_switches:
            self.rate_limited_switches.append(switch_id)
            print "\n\n ------------------- \n", "rate limiting ", switch_id, "\n-------------------"
            subprocess.call(["sudo", "ovs-vsctl", "set", "interface", switch + "-eth" + str(in_port), ingressPolicingBurst])
            subprocess.call(["sudo", "ovs-vsctl", "set", "interface", switch + "-eth" + str(in_port), ingressPolicingRate])

    def revoke_rate_limiting(self, switch, in_port, out_port, rate):
        switch_id = switch + "-eth" + str(in_port) + str(out_port)
        ingressPolicingBurst, ingressPolicingRate = "ingress_policing_burst=0", "ingress_policing_rate=0"
        if switch_id in self.rate_limited_switches:
            self.rate_limited_switches.remove(switch_id)
            print "\n\n ------------------- \n", "undo rate limiting ", switch_id, "\n-------------------"
            subprocess.call(["sudo", "ovs-vsctl", "set", "interface", switch + "-eth" + str(in_port), ingressPolicingBurst])
            subprocess.call(["sudo", "ovs-vsctl", "set", "interface", switch + "-eth" + str(in_port), ingressPolicingRate])
    # Handler for receipt of flow statistics
    # Main entry point for our DDoS detection code.
    @set_ev_cls(ofp_event.EventOFPFlowStatsReply, MAIN_DISPATCHER)
    def _flow_stats_reply_handler(self, ev):
        body = ev.msg.body
        dpid = int(ev.msg.datapath.id)
        switch = self.dpids[dpid]
        print "-------------- Flow stats for switch", switch, "---------------"

        # Iterate through all statistics reported for the flow
        for stat in sorted([flow for flow in body if flow.priority == 1], key=lambda flow: (flow.match['in_port'], flow.match['eth_dst'])):
            in_port = stat.match['in_port']
            out_port = stat.instructions[0].actions[0].port
            eth_dst = stat.match['eth_dst']

            # Check if we have a previous byte count reading for this flow
            # and calculate bandwith usage over the last polling interval
            key = (dpid, in_port, eth_dst, out_port)
            rate = 0
            if key in self.flow_byte_counts:
                cnt = self.flow_byte_counts[key]
                rate = self.bitrate(stat.byte_count - cnt)

            self.flow_byte_counts[key] = stat.byte_count
            print "In Port %8x Eth Dst %17s Out Port %8x Bitrate %f" % (in_port, eth_dst, out_port, rate)

            switch_id = switch + "-eth" + str(in_port)
            if rate > self.bw_threshold:
                if not switch_id in self.switch_interfaces:
                    self.apply_rate_limiting(switch, in_port, out_port, rate)
            elif rate < self.bw_min:
                if not switch_id in self.switch_interfaces:
                    self.revoke_rate_limiting(switch, in_port, out_port, rate)

    @set_ev_cls(ofp_event.EventOFPStateChange,[MAIN_DISPATCHER, DEAD_DISPATCHER])
    def _state_change_handler(self, ev):
        datapath = ev.datapath
        if ev.state == MAIN_DISPATCHER:
            if not datapath.id in self.datapaths:
                self.datapaths[datapath.id] = datapath
        elif ev.state == DEAD_DISPATCHER:
            if datapath.id in self.datapaths:
                del self.datapaths[datapath.id]

    def _request_stats(self, datapath):
        print 'send stats request: %016x', datapath.id
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        req = parser.OFPFlowStatsRequest(datapath)
        datapath.send_msg(req)

        req = parser.OFPPortStatsRequest(datapath, 0, ofproto.OFPP_ANY)
        datapath.send_msg(req)

    # Convert from byte count delta to bitrate
    def bitrate(self, bytes):
        return bytes * 8.0 / (self.query_interval * 1024)

    def _monitor(self):
        print "monitor..."
        while True:
            print "monitor datapaths = ", self.datapaths.values()
            for dp in self.datapaths.values():
                 self._request_stats(dp)
            hub.sleep(self.query_interval)
