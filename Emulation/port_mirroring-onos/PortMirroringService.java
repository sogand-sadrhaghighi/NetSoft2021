package edu.ucalgary.port_mirroring;

import java.util.Map;

public interface PortMirroringService {

    RouteId addFlowMirroringRules(MirroredFlowRequest<String> mirroredFlowRequest);

    RouteId addPortMirroringRules(MirroredPortsRequest<String> mirroredPortsRequest);

    void removeFlowMirroringRules(RouteId routeId);

    Map<String, Long> getSwitchMirroringPorts();
}
