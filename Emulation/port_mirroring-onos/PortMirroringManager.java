/*
 * Copyright 2019-present Open Networking Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
package edu.ucalgary.port_mirroring;

import org.apache.felix.scr.annotations.Activate;
import org.apache.felix.scr.annotations.Component;
import org.apache.felix.scr.annotations.Deactivate;
import org.apache.felix.scr.annotations.Service;
import org.apache.felix.scr.annotations.Reference;
import org.apache.felix.scr.annotations.ReferenceCardinality;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.onosproject.core.ApplicationId;
import org.onosproject.core.CoreService;

import org.onosproject.net.flowobjective.FlowObjectiveService;
import org.onosproject.net.flowobjective.ForwardingObjective;
import org.onosproject.net.flowobjective.DefaultForwardingObjective;
import org.onosproject.net.flow.TrafficTreatment;
import org.onosproject.net.flow.DefaultTrafficTreatment;
import org.onosproject.net.flow.TrafficSelector;
import org.onosproject.net.flow.DefaultTrafficSelector;
import org.onosproject.net.DeviceId;
import org.onosproject.net.device.DeviceService;
import org.onosproject.net.Port;
import org.onosproject.net.PortNumber;
import org.onosproject.net.host.HostService;
import org.onosproject.net.Host;
import org.onosproject.net.HostLocation;
import org.onosproject.net.link.LinkService;
import org.onosproject.net.Link;
import org.onosproject.net.ElementId;
import org.onosproject.net.Device;

import java.util.List;
import java.util.ArrayList;
import java.util.Set;
import java.util.HashSet;
import java.util.Optional;
import java.util.Formatter;
import java.util.Map;
import java.util.HashMap;

import java.lang.StringBuilder;
import java.lang.Iterable;

import org.onlab.packet.IpAddress;
import org.onlab.packet.MacAddress;

import fj.data.Either;

import com.google.common.collect.ListMultimap;
import com.google.common.collect.ArrayListMultimap;

/**
 * Skeletal ONOS application component.
 */
@Component(immediate = true)
@Service
public class PortMirroringManager implements PortMirroringService {

    private final Logger log = LoggerFactory.getLogger(getClass());

    private ApplicationId appId;

    private static final IpAddress DNS_SERVER_IP_ADDR           = IpAddress.valueOf("10.10.0.1");
    private static final IpAddress AGGREGATION_SERVER_IP_ADDR   = IpAddress.valueOf("10.10.0.18");

    private static final int DEFAULT_PORT_MIRRORING_FLOW_PRIORITY = 20000;

    private Map<RouteId, MirroredFlow> activeFlows;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected CoreService coreService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected FlowObjectiveService flowObjectiveService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected LinkService linkService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected HostService hostService;

    @Reference(cardinality = ReferenceCardinality.MANDATORY_UNARY)
    protected DeviceService deviceService;

    @Activate
    protected void activate() {
        log.info("Started port mirroring service.");
        appId = coreService.getAppId("edu.ucalgary.port-mirroring");
        
        activeFlows = new HashMap<RouteId, MirroredFlow>();

        checkThatAllSwitchesAreConnectedToCollector();
        configureCollectorRulesForSwitch();
    }

    @Deactivate
    protected void deactivate() {
        log.info("Stopped port mirroring service.");
        removeAllMirroredFlows();
    }
    
    public RouteId addFlowMirroringRules(MirroredFlowRequest<String> mirroredFlowRequest) {
        // Need to do two things to facilitate "flow" mirroring
        // (1) Configure rules to route traffic from source to destination.
        // (2) Configure rules to mirror traffic to aggregation server on a particular switch
        ListMultimap<DeviceId, ForwardingObjective> objectives =
            buildForwardingObjectivesFor(mirroredFlowRequest);
        addAllObjectives(objectives);
        MirroredFlow mirroredFlow = new MirroredFlow()
            .setForwardingObjectives(objectives);
        RouteId routeId = new RouteId(new Integer(mirroredFlowRequest.hashCode()).toString());
        trackMirroredFlow(routeId, mirroredFlow);
        return routeId; 
    }

    public RouteId addPortMirroringRules(MirroredPortsRequest<String> mirroredPortsRequest) {
        ListMultimap<DeviceId, ForwardingObjective> objectives = 
            buildForwardingObjectivesFor(mirroredPortsRequest);
        addAllObjectives(objectives);
        MirroredFlow mirroredFlow = new MirroredFlow()
            .setForwardingObjectives(objectives);
        RouteId routeId = new RouteId(new Integer(mirroredPortsRequest.hashCode()).toString());
        trackMirroredFlow(routeId, mirroredFlow);
        return routeId;
    }

    public void removeFlowMirroringRules(RouteId flowId) {
        MirroredFlow flowToRemove = untrackMirroredFlow(flowId)
            .orElseThrow(() -> buildFlowNotFoundExceptionFor(flowId));
        ListMultimap<DeviceId, ForwardingObjective> objectives = 
            flowToRemove.getForwardingObjectives();
        removeAllObjectives(objectives);
        log.info("Removed mirrored flow with ID {}", flowId.toString());
    }

    public Map<String, Long> getSwitchMirroringPorts() {
        Map<String, Long> mirroringPorts = new HashMap<String, Long>();
        for (Device device : deviceService.getAvailableDevices()) {
            DeviceId deviceId           = device.id();
            PortNumber mirroringPort    = getMirroringPort(deviceId);
            mirroringPorts.put(deviceId.toString(), new Long(mirroringPort.toLong()));
        }
        return mirroringPorts;
    }

    private void trackMirroredFlow(RouteId routeId, MirroredFlow flowToTrack) {
        activeFlows.put(routeId, flowToTrack);
    }

    private Optional<MirroredFlow> untrackMirroredFlow(RouteId routeId) {
        if (!activeFlows.containsKey(routeId)) {
            return Optional.empty();
        }

        MirroredFlow theMirroredFlow = activeFlows.remove(routeId);
        return Optional.of(theMirroredFlow);
    }

    private void removeAllMirroredFlows() {
        for (Map.Entry<RouteId, MirroredFlow> kvp : activeFlows.entrySet()) {
            log.info("Removed mirrored flow with ID %s", kvp.getKey().toString());
            ListMultimap<DeviceId, ForwardingObjective> objectives = 
                kvp.getValue().getForwardingObjectives();
            removeAllObjectives(objectives);
        }
    }

    private void configureCollectorRulesForSwitch() {
        DeviceId collectorSwitchDeviceId = getUplinkSwitchForHostWithIp(AGGREGATION_SERVER_IP_ADDR)
            .orElseThrow(() -> buildUplinkSwitchNotFoundException(AGGREGATION_SERVER_IP_ADDR));
        Host collectorHost = getHostWithIp(AGGREGATION_SERVER_IP_ADDR)
            .orElseThrow(() -> buildHostNotFoundExceptionFor(AGGREGATION_SERVER_IP_ADDR));
        MacAddress collectorHostMac = collectorHost.mac();

        PortNumber outputPortNumber = collectorHost.location().port();

        TrafficSelector selector = DefaultTrafficSelector.builder()
            .matchEthDst(collectorHostMac)
            .build();

        TrafficTreatment treatment = DefaultTrafficTreatment.builder()
            .setOutput(outputPortNumber)
            .build();

        ForwardingObjective objective = DefaultForwardingObjective.builder()
            .withSelector(selector)
            .withTreatment(treatment)
            .withPriority(DEFAULT_PORT_MIRRORING_FLOW_PRIORITY)
            .withFlag(ForwardingObjective.Flag.VERSATILE)
            .fromApp(appId)
            .add();

        flowObjectiveService.forward(collectorSwitchDeviceId, objective);

        ListMultimap<DeviceId, ForwardingObjective> collectorObjectiveMap = 
            ArrayListMultimap.create();
        collectorObjectiveMap.put(collectorSwitchDeviceId, objective);
        MirroredFlow collectorFlow = new MirroredFlow()
            .setForwardingObjectives(collectorObjectiveMap);
        RouteId collectorRouteId = new RouteId(new Integer(collectorFlow.hashCode()).toString());
        trackMirroredFlow(collectorRouteId, collectorFlow);
        log.info("Successfully installed collector flow rules.");
    }

    private void checkThatAllSwitchesAreConnectedToCollector() {
        DeviceId collectorSwitchId = getUplinkSwitchForHostWithIp(AGGREGATION_SERVER_IP_ADDR)
            .orElseThrow(() -> buildUplinkSwitchNotFoundException(AGGREGATION_SERVER_IP_ADDR));
        Set<DeviceId> allSwitches = new HashSet<DeviceId>();
        for (Device device : deviceService.getAvailableDevices()) {
            if (!device.id().equals(collectorSwitchId)) {
                allSwitches.add(device.id());
            }
        }
        for (DeviceId deviceId : allSwitches) {
            getConnectingLink(deviceId, collectorSwitchId)
                .orElseThrow(() -> buildNotConnectedToCollectorExceptionFor(deviceId));
        }
    }

    private PortNumber getMirroringPort(DeviceId sourceSwitchId) {
        DeviceId collectorSwitchId = getUplinkSwitchForHostWithIp(AGGREGATION_SERVER_IP_ADDR)
            .orElseThrow(() -> buildUplinkSwitchNotFoundException(AGGREGATION_SERVER_IP_ADDR));
        Link mirroringLink = getConnectingLink(sourceSwitchId, collectorSwitchId)
            .orElseThrow(() -> buildNotConnectedToCollectorExceptionFor(sourceSwitchId));
        return mirroringLink.src().port();
    }

    private Optional<Link> getConnectingLink(DeviceId sourceId, ElementId destinationId) {
        Set<Link> sourceLinks = linkService.getDeviceLinks(sourceId);
        for (Link link : sourceLinks) {
            if (link.dst().elementId().equals(destinationId)) {
                return Optional.of(link);
            }
        }
        return Optional.empty();
    }

    private UnsupportedOperationException buildNotConnectedToCollectorExceptionFor(
            DeviceId switchId) {
        StringBuilder sb = new StringBuilder();
        Formatter fmt = new Formatter(sb);
        fmt.format("Switch %s is not connected to the collector switch. Unable to perform port mirroring.", switchId.toString());
        String errorString = fmt.toString();
        log.error(errorString);
        UnsupportedOperationException ex = new UnsupportedOperationException(errorString);
        return ex;
    }

    private UnsupportedOperationException buildHostNotFoundExceptionFor(IpAddress ipAddress) {
        StringBuilder sb = new StringBuilder();
        Formatter fmt = new Formatter(sb);
        fmt.format("Couldn't find host with IP %s", ipAddress.toString());
        String errorString = fmt.toString();
        log.error(errorString);
        UnsupportedOperationException ex = new UnsupportedOperationException(errorString);
        return ex;
    }

    private UnsupportedOperationException buildFlowNotFoundExceptionFor(RouteId routeId) {
        StringBuilder sb = new StringBuilder();
        Formatter fmt = new Formatter(sb);
        fmt.format("No record of state for flow rule with ID %s", routeId.toString());
        String errorString = fmt.toString();
        log.error(errorString);
        UnsupportedOperationException ex = new UnsupportedOperationException(errorString);
        return ex;
    }

    private Optional<DeviceId> getUplinkSwitchForHostWithIp(IpAddress hostIp) {
        Optional<Host> maybeHost = getHostWithIp(hostIp);
        if (maybeHost.isPresent()) {
            HostLocation hostLocation = maybeHost.get().location();
            return Optional.of(hostLocation.deviceId());
        } else {
            return Optional.empty();
        }
    }

    private Optional<Host> getHostWithIp(IpAddress ipAddress) {
        Set<Host> hostsWithIp = hostService.getHostsByIp(ipAddress);
        if (hostsWithIp.size() != 1) {
            return Optional.empty();
        } else {
            return Optional.of(hostsWithIp.iterator().next());
        }
    }

    private UnsupportedOperationException buildUplinkSwitchNotFoundException(IpAddress hostIp) {
        StringBuilder sb = new StringBuilder();
        Formatter fmt = new Formatter(sb);
        fmt.format("Failed to find uplink switch for host with IP %s", hostIp.toString());
        String errorString = fmt.toString();
        log.error(errorString);
        UnsupportedOperationException ex = new UnsupportedOperationException(errorString);
        return ex;
    }

    private ListMultimap<DeviceId, ForwardingObjective>
        buildForwardingObjectivesFor(MirroredPortsRequest<String> mirroredPortsRequest) {
        // Should do this on a switch by switch basis. 
        // for each switch s_i in the network do the following:
        //  * Compute set of flows, F, that transit s_i.
        //  * Compute ingress and egress ports on s_i for each f_i \in F, call this results P
        //  * Compute intersection of mirrored ports on s_i, M_i, and P
        //  * for f_i with M_i intersect P_i not empty install mirroring flows 
        //  * for f_i with M_i intersect P_i empty install regular flows
        
        List<DeviceId> switchIds = new ArrayList<DeviceId>();
        for (String nodeId : mirroredPortsRequest.getFlowRoute().getNodes()) {
            DeviceId switchId = DeviceId.deviceId(nodeId);
            switchIds.add(switchId);
        }

        ListMultimap<DeviceId, PortNumber> mirroredPortNumbers = ArrayListMultimap.create();
        for (Map.Entry<String, List<Integer>> kvp : 
                mirroredPortsRequest.getMirroredPorts().entrySet()) {
            DeviceId switchId = DeviceId.deviceId(kvp.getKey());
            for (Integer portId : kvp.getValue()) {
                PortNumber portNumber = PortNumber.portNumber(portId);
                mirroredPortNumbers.put(switchId, portNumber);
            }
        }

        ListMultimap<DeviceId, ForwardingObjective> objectives = ArrayListMultimap.create();
        DeviceId flowSourceId           = switchIds.get(0);
        DeviceId flowDestinationId      = switchIds.get(switchIds.size() - 1);
        boolean hasBeenMirrored         = false;
        
        Host sourceHost = getConnectedHost(flowSourceId)
            .orElseThrow(() -> buildHostNotFoundExceptionFor(flowSourceId));
        Host destinationHost = getConnectedHost(flowDestinationId)
            .orElseThrow(() -> buildHostNotFoundExceptionFor(flowDestinationId));

        Host collectorHost = getHostWithIp(AGGREGATION_SERVER_IP_ADDR)
            .orElseThrow(() -> buildHostNotFoundExceptionFor(AGGREGATION_SERVER_IP_ADDR));
        MacAddress collectorMacAddr = collectorHost.mac();

        TrafficSelector trafficSelector = DefaultTrafficSelector.builder()
            .matchEthType((short) 0x0800)
            .matchEthSrc(sourceHost.mac())
            .matchEthDst(destinationHost.mac())
            .matchIPProtocol((byte) 17)
            .matchIPDscp((byte) mirroredPortsRequest.getTagValue())
            .build();
        
        // Loop through list of switches.
        //  * check if mirroredPortNumbers contains the switchId in question.
        //  * check if the flow is ingress or egress on any of those ports.
        //      * if it is add mirroring + routing rules
        //      * if it isn't add routing rules
        for (int switchIdx = 0; switchIdx < switchIds.size(); switchIdx++) {
            DeviceId switchId = switchIds.get(switchIdx);
            TrafficTreatment.Builder treatmentBuilder = DefaultTrafficTreatment.builder();

            PortNumber outputPort = null;
            if (switchIdx == (switchIds.size() - 1)) {
                outputPort = destinationHost.location().port();
            } else {
                DeviceId nextHopSwitchId = switchIds.get(switchIdx + 1);
                Link theLink = getConnectingLink(switchId, nextHopSwitchId)
                    .orElseThrow(() -> buildUnfoundLinkExceptionFor(switchId, nextHopSwitchId,
                                flowSourceId, flowDestinationId));
                outputPort = theLink.src().port();
                PortNumber targetPortNumber = PortNumber.portNumber(
                        mirroredPortsRequest.getPortNumbers().get(switchIdx));
                if (!targetPortNumber.equals(outputPort)) {
                    log.error("Actual output port does not match target output port!!!");
                }
            }

            PortNumber inputPort = null;
            if (switchIdx == 0) {
                inputPort = sourceHost.location().port();
            } else {
                DeviceId previousHopSwitchId = switchIds.get(switchIdx - 1);
                Link theLink = getConnectingLink(previousHopSwitchId, switchId)
                    .orElseThrow(() -> buildUnfoundLinkExceptionFor(previousHopSwitchId,
                                switchId, flowSourceId, flowDestinationId));
                inputPort = theLink.dst().port();
            }

            treatmentBuilder.setOutput(outputPort);
            PortNumber switchMirroringPort = getMirroringPort(switchId);
            boolean isInputPortMirrored     = mirroredPortNumbers.containsEntry(switchId, inputPort);
            boolean isOutputPortMirrored    = mirroredPortNumbers.containsEntry(switchId, 
                    outputPort);
            // if (isInputPortMirrored || isOutputPortMirrored) {
            //     treatmentBuilder.setEthDst(collectorMacAddr);
            //     hasBeenMirrored = true;
            // }
            
            if (isOutputPortMirrored) {
                treatmentBuilder.setEthDst(collectorMacAddr);
                hasBeenMirrored = true;
            }

            if (isInputPortMirrored && isOutputPortMirrored) {
                log.info("Both ports mirrored");
            } else if (isInputPortMirrored) {
                log.info("Input port mirrored");
            } else if (isOutputPortMirrored) {
                log.info("Output port mirrored");
            } else {
                log.error("No ports mirrored");
            }

            if (isInputPortMirrored) {
                // treatmentBuilder.setOutput(switchMirroringPort);
            }
            if (isOutputPortMirrored) {
                treatmentBuilder.setOutput(switchMirroringPort);
            }

            TrafficTreatment trafficTreatment = treatmentBuilder.build();
            ForwardingObjective objective = DefaultForwardingObjective.builder()
                .withSelector(trafficSelector)
                .withTreatment(trafficTreatment)
                .withPriority(DEFAULT_PORT_MIRRORING_FLOW_PRIORITY)
                .withFlag(ForwardingObjective.Flag.VERSATILE)
                .fromApp(appId)
                .add();
            objectives.put(switchId, objective);
        }
        if (!hasBeenMirrored) {
            log.error("FLOW HAS NOT BEEN MIRRORED");
        }
        return objectives;
    }

    private ListMultimap<DeviceId, ForwardingObjective> 
        buildForwardingObjectivesFor(MirroredFlowRequest<String> mirroredFlowRequest) {
        List<DeviceId> switchIds = new ArrayList<DeviceId>();
        for (String nodeId : mirroredFlowRequest.getFlowRoute().getNodes()) { 
            DeviceId switchId = DeviceId.deviceId(nodeId);
            switchIds.add(switchId);
        }

        ListMultimap<DeviceId, ForwardingObjective> objectives = 
            ArrayListMultimap.create();
        DeviceId flowSourceId           = switchIds.get(0);
        DeviceId flowDestinationId      = switchIds.get(switchIds.size() - 1);
        DeviceId mirrorDeviceId         = DeviceId.deviceId(mirroredFlowRequest.getMirrorSwitch());

        Host sourceHost = getConnectedHost(flowSourceId)
            .orElseThrow(() -> buildHostNotFoundExceptionFor(flowSourceId));
        Host destinationHost = getConnectedHost(flowDestinationId)
            .orElseThrow(() -> buildHostNotFoundExceptionFor(flowDestinationId));
        MacAddress sourceMacAddress = sourceHost.mac();
        MacAddress destinationMacAddress = destinationHost.mac();
        
        Host collectorHost = getHostWithIp(AGGREGATION_SERVER_IP_ADDR)
            .orElseThrow(() -> buildHostNotFoundExceptionFor(AGGREGATION_SERVER_IP_ADDR));
        MacAddress collectorMacAddr = collectorHost.mac();

        ForwardingObjectiveBuilder theBuilder = null;
        for (int switchIdx = 0; switchIdx < switchIds.size(); switchIdx++) {
            DeviceId switchId = switchIds.get(switchIdx);
            if (switchId.equals(mirrorDeviceId)) {
                theBuilder = (deviceId, flowRequest, outputPort) -> 
                    buildForwardingObjectiveWithMirroringFor(deviceId, 
                            flowRequest, outputPort, collectorMacAddr, sourceMacAddress, destinationMacAddress);
            } else {
                theBuilder = (deviceId, flowRequest, outputPort) -> 
                    buildForwardingObjectiveFor(deviceId, flowRequest, outputPort, sourceMacAddress, destinationMacAddress);
            }

            ForwardingObjective objective = null;
            if (switchIdx == (switchIds.size() - 1)) {
                objective = theBuilder.buildForwardingObjective(switchId, mirroredFlowRequest, 
                        destinationHost.location().port());
            } else {
                DeviceId nextHopSwitchId = switchIds.get(switchIdx + 1);
                Link theLink = getConnectingLink(switchId, nextHopSwitchId)
                    .orElseThrow(() -> buildUnfoundLinkExceptionFor(switchId, nextHopSwitchId,
                                flowSourceId, flowDestinationId));
                objective = theBuilder.buildForwardingObjective(switchId, 
                        mirroredFlowRequest, theLink.src().port());
            }
            objectives.put(switchId, objective);
        }

        return objectives;
    }

    private ForwardingObjective 
        buildForwardingObjectiveFor( DeviceId switchId
                                   , MirroredFlowRequest<String> mirroredFlowRequest
                                   , PortNumber outputPort
                                   , MacAddress sourceMacAddress
                                   , MacAddress destinationMacAddress) {
        TrafficSelector trafficSelector = DefaultTrafficSelector.builder()
            .matchEthType((short) 0x0800)
            .matchEthSrc(sourceMacAddress)
            .matchEthDst(destinationMacAddress)
            .matchIPProtocol((byte) 17)
            .matchIPDscp((byte) mirroredFlowRequest.getTagValue())
            .build();

        TrafficTreatment trafficTreatment = DefaultTrafficTreatment.builder()
            .setOutput(outputPort)
            .build();

        ForwardingObjective objective = DefaultForwardingObjective.builder()
            .withSelector(trafficSelector)
            .withTreatment(trafficTreatment)
            .withPriority(DEFAULT_PORT_MIRRORING_FLOW_PRIORITY)
            .withFlag(ForwardingObjective.Flag.VERSATILE)
            .fromApp(appId)
            .add();

        return objective;
    }

    private ForwardingObjective
        buildForwardingObjectiveWithMirroringFor( DeviceId switchId
                                                , MirroredFlowRequest<String> mirroredFlowRequest
                                                , PortNumber outputPort
                                                , MacAddress collectorMacAddr
                                                , MacAddress sourceMacAddress
                                                , MacAddress destinationMacAddress) {
        TrafficSelector trafficSelector = DefaultTrafficSelector.builder()
            .matchEthType((short) 0x0800)
            .matchEthSrc(sourceMacAddress)
            .matchEthDst(destinationMacAddress)
            .matchIPProtocol((byte) 17)
            .matchIPDscp((byte) mirroredFlowRequest.getTagValue())
            .build();

        PortNumber switchMirroringPort = getMirroringPort(switchId);
        TrafficTreatment trafficTreatment = DefaultTrafficTreatment.builder()
            .setOutput(outputPort)
            .setEthDst(collectorMacAddr)
            .setOutput(switchMirroringPort)
            .build();

        ForwardingObjective objective = DefaultForwardingObjective.builder()
            .withSelector(trafficSelector)
            .withTreatment(trafficTreatment)
            .withPriority(DEFAULT_PORT_MIRRORING_FLOW_PRIORITY)
            .withFlag(ForwardingObjective.Flag.VERSATILE)
            .fromApp(appId)
            .add();

        return objective;
    }

    private Optional<Link> getConnectingLink(DeviceId sourceId, DeviceId destinationId) {
        Set<Link> sourceLinks = linkService.getDeviceLinks(sourceId);
        for (Link link : sourceLinks) {
            if (link.dst().deviceId().equals(destinationId)) {
                return Optional.of(link);
            }
        }
        return Optional.empty();
    }

    private Optional<Host> getConnectedHost(DeviceId switchId) {
        Set<Host> connectedHosts = hostService.getConnectedHosts(switchId);

        for (Host theHost : connectedHosts) {
            if (!theHost.ipAddresses().contains(DNS_SERVER_IP_ADDR)) {
                return Optional.of(theHost);
            }
        }

        return Optional.empty();
    }

    private UnsupportedOperationException buildUnfoundLinkExceptionFor( DeviceId sourceId
                                                                      , DeviceId destinationId
                                                                      , DeviceId pathSourceId
                                                                      , DeviceId pathDestinationId) {
        StringBuilder sb = new StringBuilder();
        Formatter fmt = new Formatter(sb);
        fmt.format("Could not find link between %s and %s while building path from %s to %s.",
                sourceId.toString(), destinationId.toString(), 
                pathSourceId.toString(), pathDestinationId.toString());
        String errorString = fmt.toString();
        log.error(errorString);
        return new UnsupportedOperationException(errorString);
    }

    private UnsupportedOperationException buildHostNotFoundExceptionFor(DeviceId switchId) {
        StringBuilder sb = new StringBuilder();
        Formatter fmt = new Formatter(sb);
        fmt.format("Could not find host attached to %s", switchId.toString());
        String errorString = fmt.toString();
        log.error(errorString);
        return new UnsupportedOperationException(errorString);
    }

    private void addAllObjectives(ListMultimap<DeviceId, ForwardingObjective> objectives) {
        for (Map.Entry<DeviceId, ForwardingObjective> kvp : objectives.entries()) {
            flowObjectiveService.forward(kvp.getKey(), kvp.getValue());
        }
    }

    private void removeAllObjectives(
            ListMultimap<DeviceId, ForwardingObjective> forwardingObjectives) {
        for (Map.Entry<DeviceId, ForwardingObjective> kvp : forwardingObjectives.entries()) {
            ForwardingObjective oldObjective = kvp.getValue();
            ForwardingObjective removeObjective = oldObjective.copy().remove();
            flowObjectiveService.forward(kvp.getKey(), removeObjective);
        }
    }

    interface ForwardingObjectiveBuilder {
        public ForwardingObjective 
            buildForwardingObjective( DeviceId switchId
                                    , MirroredFlowRequest<String> mirroredFlowRequest
                                    , PortNumber outputPort);
    }
}
