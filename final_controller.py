
from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Final (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

  def do_final (self, packet, packet_in, port_on_switch, switch_id):


    match = of.ofp_match.from_packet(packet_in)#match data from current packet event

    print "The nw_proto is: ", match.nw_proto

    Src = str(match.nw_src)
    Dst = str(match.nw_dst)

    h1ip = "10.0.1.101"
    h2ip = "10.0.2.102"
    h3ip = "10.0.3.103"
    h4ip = "128.114.50.10"#Untrusted Host ip address
    h5ip = "10.0.4.104"#Server Host ip address

    ip = 0x0800 #check against match.dl_type
    icmp = 1 #check against match.nw_proto

    msg = of.ofp_packet_out(data=packet_in)
    msg2 = of.ofp_flow_mod()

    def send(outPort, ipSrc, ipDst, inPort, pktType, pktProto):

      msg2.match.dl_type = pktType
      msg2.match.nw_proto = pktProto
      msg2.match.nw_src = ipSrc
      msg2.match.nw_dst = ipDst
      msg2.match.in_port = inPort
      msg2.hard_timeout = 300
      msg2.idle_timeout = 120


      if (outPort == -1):

        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        self.connection.send(msg)

        msg2.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        self.connection.send(msg2)

      elif (outPort == -2):
      
        #msg.actions.append(of.ofp_action_output())
        self.connection.send(msg)

        #msg2.actions.append(of.ofp_action_output())
        self.connection.send(msg2)

      else:

        msg.actions.append(of.ofp_action_output(port=outPort))
        self.connection.send(msg)

        msg2.actions.append(of.ofp_action_output(port=outPort))
        self.connection.send(msg2)

    #Implementing controller logic via if-elif-else tree.    

    if (switch_id == 1 or switch_id == 2 or switch_id == 3 or switch_id == 5):
    
      if (port_on_switch == 1):

        send(2, None, None, match.in_port, None, None)

      else:

        send(1, None, None, match.in_port, None, None)


    elif (switch_id == 4):

      if (match.dl_type != ip):

        send(-1, match.nw_src, match.nw_dst, match.in_port, match.dl_type, match.nw_proto) 

      else:


        if ((Src == h4ip and match.nw_proto == icmp) or (Src == h4ip and Dst == h5ip)):

          if (match.nw_proto == icmp):

            send(-2, match.nw_src, match.nw_dst, match.in_port, match.dl_type, match.nw_proto)

          else:

            send(-2, match.nw_src, match.nw_dst, match.in_port, match.dl_type, None)  

        elif (Src == h4ip and match.dl_type == ip and match.nw_proto != icmp and Dst != h5ip):

          print "snoogens", "The protocol is: ", match.nw_proto

          if (Dst == h1ip):

            send(1, None, match.nw_dst, match.in_port, match.dl_type, match.nw_proto)

          elif (Dst == h2ip):

            send(2, None, match.nw_dst, match.in_port, match.dl_type, match.nw_proto)

          else:

            send(3, None, match.nw_dst, match.in_port, match.dl_type, match.nw_proto) 

        elif (Src != h4ip and match.dl_type == ip):

          if (Dst == h1ip):

            send(1, None, match.nw_dst, match.in_port, match.dl_type, match.nw_proto)

          elif (Dst == h2ip):

            send(2, None, match.nw_dst, match.in_port, match.dl_type, match.nw_proto)

          elif (Dst == h3ip):

            send(3, None, match.nw_dst, match.in_port, match.dl_type, match.nw_proto)

          elif (Dst == h4ip):
        
            send(4, None, match.nw_dst, match.in_port, match.dl_type, match.nw_proto)  

          else:
        
            send(5, None, match.nw_dst, match.in_port, match.dl_type, match.nw_proto) 

        #elif (match.dl_type != ip):
      
          #send(-1, match.nw_src, match.nw_dst, match.in_port, match.dl_type, match.nw_proto)       
      


            
    


  


        






  def _handle_PacketIn (self, event):
    """
    Handles packet in messages from the switch.
    """
    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    self.do_final(packet, packet_in, event.port, event.dpid)

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Final(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)