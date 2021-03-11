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

import com.fasterxml.jackson.databind.node.ObjectNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.core.type.TypeReference;
import org.onosproject.rest.AbstractWebResource;

import javax.ws.rs.GET;
import javax.ws.rs.POST;
import javax.ws.rs.Consumes;
import javax.ws.rs.Path;
import javax.ws.rs.QueryParam;
import javax.ws.rs.core.Response;
import javax.ws.rs.core.MediaType;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import fj.data.Either;

import java.io.InputStream;

import java.util.Map;

import static org.onlab.util.Tools.nullIsNotFound;

/**
 * Sample web resource.
 */
@Path("/v1")
public class AppWebResource extends AbstractWebResource {

    private static Logger log = LoggerFactory.getLogger(AbstractWebResource.class);
    
    @POST
    @Path("/add-mirrored-flow/")
    @Consumes(MediaType.APPLICATION_JSON)
    public Response addMirroredFlow(InputStream bodyStream) {
        Response response = maybeParseAddMirroredFlowRequest(bodyStream)
            .right()
            .map((flowRequest) -> {
                log.info("Recieved MirroredFlowRequest: {}", flowRequest.toString());
                RouteId routeId = null;
                PortMirroringService portMirroringService = get(PortMirroringService.class);
                try {
                    routeId = portMirroringService.addFlowMirroringRules(flowRequest);
                } catch (Exception ex) {
                    log.error("addFlowMirroringRules failed", ex);
                    return buildErrorResponse(ex);
                }
                return buildSuccessResponse(routeId);
            })
            .right()
            .on((ex) -> buildErrorResponse(ex));
            
        return response;
    }

    @POST
    @Path("/add-mirrored-ports/")
    @Consumes(MediaType.APPLICATION_JSON)
    public Response addMirroredPorts(InputStream bodyStream) {
        Response response = maybeParseAddMirroredPortsRequest(bodyStream)
            .right()
            .map((mirroredPortsRequest) -> {
                log.info("Received MirroredPortsRequest: {}", mirroredPortsRequest.toString());
                RouteId routeId = null;
                PortMirroringService portMirroringService = get(PortMirroringService.class);
                try {
                    routeId = portMirroringService.addPortMirroringRules(mirroredPortsRequest);
                } catch (Exception ex) {
                    log.error("addPortMirroringRules failed", ex);
                    return buildErrorResponse(ex);
                }
                return buildSuccessResponse(routeId);
            })
            .right()
            .on((ex) -> buildErrorResponse(ex));

        return response;
    }

    @POST
    @Path("/remove-mirrored-flow/")
    public Response removeMirroredFlow(@QueryParam("route-id") String routeIdString) {
        log.info("Received remove mirrored flow request for route id {}", routeIdString);
        RouteId routeId = RouteId.fromString(routeIdString);
        PortMirroringService portMirroringService = get(PortMirroringService.class);
        // @TODO: Refactor this to be more inline with the way that errors are handled 
        // in the rest of the codebase.
        try {
            portMirroringService.removeFlowMirroringRules(routeId);
        } catch (Exception ex) {
            Response errorResponse = buildErrorResponse(ex);
            return errorResponse;
        }

        Response successResponse = 
            buildSuccessResponse("Removed mirroring flows with id " + routeIdString);
        return successResponse;
    }

    @GET
    @Path("/mirroring-ports/")
    public Response getSwitchMirroringPorts() {
        log.info("Received mirroring-ports request.");
        PortMirroringService portMirroringService = get(PortMirroringService.class);
        Map<String, Long> switchMirroringPorts = null;
        try {
            switchMirroringPorts = portMirroringService.getSwitchMirroringPorts();
        } catch (Exception ex) {
            Response errorResponse = buildErrorResponse(ex);
            return errorResponse;
        }

        Response successResponse = 
            buildSuccessResponse(switchMirroringPorts);
        return successResponse;
    }

    private Either<java.io.IOException, MirroredFlowRequest<String>>
        maybeParseAddMirroredFlowRequest(InputStream reqBodyInputStream) {
        ObjectMapper objMapper = new ObjectMapper();
        MirroredFlowRequest<String> mirroredFlowRequest = null;
        try {
            mirroredFlowRequest = objMapper.readValue(reqBodyInputStream,
                    new TypeReference<MirroredFlowRequest<String>>() { });
        } catch (java.io.IOException ex) {
            return Either.left(ex);
        }
        return Either.right(mirroredFlowRequest);
    }

    private Either<java.io.IOException, MirroredPortsRequest<String>>
        maybeParseAddMirroredPortsRequest(InputStream reqBodyInputStream) {
        ObjectMapper objMapper = new ObjectMapper();
        MirroredPortsRequest<String> mirroredPortsRequest = null;
        try {
            mirroredPortsRequest = objMapper.readValue(reqBodyInputStream,
                    new TypeReference<MirroredPortsRequest<String>>() { });
        } catch (java.io.IOException ex) {
            return Either.left(ex);
        }
        return Either.right(mirroredPortsRequest);
    }

    private Response buildErrorResponse(Exception ex) {
        Response errResponse = Response
            .status(Response.Status.INTERNAL_SERVER_ERROR)
            .entity(ex.getMessage())
            .build();
        return errResponse;
    }

    private Response buildSuccessResponse(RouteId routeId) {
        ObjectNode node = mapper().createObjectNode().put("routeId", routeId.toString());
        Response successResponse = ok(node).build();
        return successResponse;
    }

    private Response buildSuccessResponse(String successMessage) {
        ObjectNode node = mapper().createObjectNode().put("message", successMessage);
        Response successResponse = ok(node).build();
        return successResponse;
    }

    private Response buildSuccessResponse(Map<String, Long> result) {
        ObjectMapper objMapper = new ObjectMapper();
        String jsonStr = null;
        try {
            jsonStr = objMapper.writerWithDefaultPrettyPrinter()
                .writeValueAsString(result);
        } catch (java.io.IOException ex) {
            return buildErrorResponse(ex);
        }
        ObjectNode node = mapper().createObjectNode().put("result", jsonStr);
        Response successResponse = ok(node).build();
        return successResponse;
    }
}

























