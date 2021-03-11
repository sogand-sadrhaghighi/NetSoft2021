package edu.ucalgary.port_mirroring;

import org.onosproject.net.flowobjective.ForwardingObjective;
import org.onosproject.net.DeviceId;

import com.google.common.collect.ListMultimap;
import com.google.common.collect.ArrayListMultimap;

public class MirroredFlow {
    private ListMultimap<DeviceId, ForwardingObjective> forwardingObjectives;
    
    public MirroredFlow() {

    }

    public ListMultimap<DeviceId, ForwardingObjective> getForwardingObjectives() {
        return this.forwardingObjectives;
    }

    public MirroredFlow setForwardingObjectives(
            ListMultimap<DeviceId, ForwardingObjective> theForwardingObjectives) {
        this.forwardingObjectives = theForwardingObjectives;
        return this;
    }
}
