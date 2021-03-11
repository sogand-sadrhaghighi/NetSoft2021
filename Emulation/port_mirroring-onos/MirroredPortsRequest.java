package edu.ucalgary.port_mirroring;

import java.util.List;
import java.util.Map;
import java.util.Formatter;

import java.lang.StringBuilder;

public class MirroredPortsRequest<NodeType> {
    private Path<NodeType>                              flowRoute;
    private List<Integer>                               portNumbers;
    private short                                       tagValue;
    private Map<NodeType, List<Integer>>                mirroredPorts;
    
    public MirroredPortsRequest() {
        this.flowRoute      = null;
        this.portNumbers    = null;
        this.tagValue       = -1;
    }

    public Path<NodeType> getFlowRoute() {
        return this.flowRoute;
    }

    public MirroredPortsRequest<NodeType> setFlowRoute(Path<NodeType> theFlowRoute) {
        this.flowRoute = theFlowRoute;
        return this;
    }

    public List<Integer> getPortNumbers() {
        return this.portNumbers;
    }

    public MirroredPortsRequest<NodeType> setPortNumbers(List<Integer> thePortNumbers) {
        this.portNumbers = thePortNumbers;
        return this;
    }

    public short getTagValue() {
        return this.tagValue;
    }
    
    public MirroredPortsRequest<NodeType> setTagValue(short theTagValue) {
        this.tagValue = theTagValue;
        return this;
    }

    public Map<NodeType, List<Integer>> getMirroredPorts() {
        return this.mirroredPorts;
    }

    public MirroredPortsRequest<NodeType> setMirroredPorts(
            Map<NodeType, List<Integer>> theMirroredPorts) {
        this.mirroredPorts = theMirroredPorts;
        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb    = new StringBuilder();
        Formatter fmt       = new Formatter(sb);
        fmt.format("MirroredPortsRequest { path: %s, mirroredPorts: %s, ports: %s }",
                getFlowRoute().toString(), getMirroredPorts().toString(),
                getPortNumbers().toString());
        return fmt.toString();
    }
}
