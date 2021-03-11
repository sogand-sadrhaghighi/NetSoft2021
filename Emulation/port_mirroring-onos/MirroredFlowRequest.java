package edu.ucalgary.port_mirroring;

import java.lang.StringBuilder;
import java.util.Formatter;

public class MirroredFlowRequest<NodeType> {
    private Path<NodeType>      flowRoute;
    private NodeType            mirrorSwitch;
    private short               tagValue;
    
    public MirroredFlowRequest() { 
        this.flowRoute          = null;
        this.mirrorSwitch       = null;
        this.tagValue           = -1;
    }

    public Path<NodeType> getFlowRoute() {
        return this.flowRoute;
    }

    public MirroredFlowRequest<NodeType> setFlowRoute(Path<NodeType> theFlowRoute) {
        this.flowRoute = theFlowRoute;
        return this;
    }
    
    public NodeType getMirrorSwitch() {
        return this.mirrorSwitch;
    }

    public MirroredFlowRequest<NodeType> setMirrorSwitch(NodeType theMirrorSwitch) {
        this.mirrorSwitch = theMirrorSwitch;
        return this;
    }

    public short getTagValue() {
        return this.tagValue;
    }

    public MirroredFlowRequest<NodeType> setTagValue(short theTagValue) {
        this.tagValue = theTagValue;
        return this;
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }

        if (!(other instanceof MirroredFlowRequest)) {
            return false;
        }

        MirroredFlowRequest otherFlowRequest = (MirroredFlowRequest) other;
        return 
            this.getFlowRoute().equals(otherFlowRequest.getFlowRoute()) &&
            this.getMirrorSwitch().equals(otherFlowRequest.getMirrorSwitch()) &&
            this.getTagValue() == otherFlowRequest.getTagValue();
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        Formatter fmt = new Formatter(sb);
        fmt.format("MirroredFlowRequest { flowRoute: %s, mirrorSwitch: %s",
                flowRoute.toString(), mirrorSwitch.toString());
        return sb.toString();
    }
}
