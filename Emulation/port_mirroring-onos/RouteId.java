package edu.ucalgary.port_mirroring;

public class RouteId {
    String routeHash;

    public RouteId(String theRouteHash) {
        this.routeHash = theRouteHash;
    }

    public String getRouteId() {
        return this.routeHash;
    }

    public RouteId setRouteId(String theRouteId) {
        this.routeHash = theRouteId;
        return this;
    }

    @Override
    public String toString() {
        return routeHash;
    }

    public static RouteId fromString(String routeHash) {
        return new RouteId(routeHash);
    }

    @Override
    public int hashCode() {
        return new Integer(routeHash);
    }

    @Override
    public boolean equals(Object other) {
        if (other == this) {
            return true;
        }

        if (!(other instanceof RouteId)) {
            return false;
        }

        RouteId otherRouteId = (RouteId) other;
        return this.getRouteId().equals(otherRouteId.getRouteId());
    }
}
