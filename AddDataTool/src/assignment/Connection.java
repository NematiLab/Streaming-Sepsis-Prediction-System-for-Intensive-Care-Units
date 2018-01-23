/**
 * Created by Joel on 9/29/2017.
 */
package assignment;

import ca.uhn.fhir.context.FhirContext;
import ca.uhn.fhir.model.primitive.UriDt;
import ca.uhn.fhir.rest.client.IGenericClient;
import org.hl7.fhir.instance.model.api.IBaseResource;

/**
 *
 */
public class Connection {

    private IGenericClient client = null;

    public Connection(String baseUrl) {
        //Place your code here
        //UriDt test = new UriDt();
        //test.setValue(baseUrl);
        //client.search(test);
        //IBaseResource res = new IBaseResource();
        //res.

        // Log the request
        FhirContext ctx = FhirContext.forDstu2();
        client = ctx.newRestfulGenericClient(baseUrl);
        //System.out.println(ctx.newXmlParser().setPrettyPrint(true).encodeResourceToString(bundle));

        // Create a client and post the transaction to the server


    }

    public IGenericClient getClient() {
        return client;
    }

}
