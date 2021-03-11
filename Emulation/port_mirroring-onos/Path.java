package edu.ucalgary.port_mirroring;

import java.util.List;

import java.util.Formatter;
import java.lang.StringBuilder;

// @TODO: Since it is possible to create objects of type Path in an 
// invalid state, should have a builder that builds Optional<Path> rather
// than directly constructing the path type. That way we have objects 
// that are guaranteed to be in a valid state if they are able to be constructed.
public class Path<NodeType> {
    private List<NodeType>  nodes;
    
    public Path() { }
    
    public Path(List<NodeType> theNodes) {
        this.nodes = theNodes; 
    }

    public List<NodeType> getNodes() {
        return this.nodes;
    }

    public Path setNodes(List<NodeType> theNodes) {
        this.nodes = theNodes;
        return this;
    }

    public boolean validatePath() {
        if (nodes.size() < 2 || this.getSourceSwitchId().equals(this.getDestinationSwitchId())) {
            return false;
        }
        return true;
    }

    public NodeType getSourceSwitchId() {
        return nodes.get(0);
    }

    public NodeType getDestinationSwitchId() {
        return nodes.get(nodes.size() - 1);
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        Formatter fmt = new Formatter(sb);
        fmt.format("{ nodes: %s }", nodes.toString());
        return sb.toString();
    }

    @Override
    public boolean equals(Object other) {
        if (this == other) {
            return true;
        }

        if (!(other instanceof Path)) {
            return false;
        }

        Path<NodeType> otherPath = (Path<NodeType>) other;
        return this.getNodes().equals(otherPath.getNodes());
    }
}





















