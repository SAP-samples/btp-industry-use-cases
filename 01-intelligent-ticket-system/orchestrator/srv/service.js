module.exports = cds.service.impl(async function () {
    // Connect to external services destinations
    const CTC = await cds.connect.to('CTC');
    const BR = await cds.connect.to('BR');
    const FSM = await cds.connect.to('FSM');

    /*** ACTION HANDLERS ***/
    this.on('handleMessage', async req => {
        try {
            // Grab message from payload
            const message = req.data.message;

            // Call CTC classification API passing the received message and retrieve classification
            const CTC_payload = {
                text: message.text 
            };
            const CTC_resp = await CTC.post("/do-analysis", CTC_payload);
            const classification = new String(CTC_resp.overall_classification);

            // Call Business Rules API passing the classification and retreive the route
            const BR_payload = {
                RuleServiceId: "3a4e53b84c8e4313bc6d7922ade85808",
                RuleServiceRevision: "1",
                Vocabulary: [
                    {
                        Classification: classification
                    }
                ]
            };
            const BR_resp = await BR.post("/rules-service/rest/v2/rule-services", BR_payload);
            const action = BR_resp.Result[0].Route.Action;
            
            // If action is "CRM" then a service request must be created
            let code = "";
            if (action === "CRM") {
                const FSM_payload = {
                    leader : null,
                    subject : message.text,
                    chargeableEfforts : false,
                    project : null,
                    owners : null,
                    objectGroup : null,
                    resolution : null,
                    syncObjectKPIs : null,
                    inactive : false,
                    partOfRecurrenceSeries : null,
                    contact : "D0725AA6243A4470A49C0052232CA898",
                    problemTypeName : null,
                    originCode : "-1",
                    problemTypeCode : null,
                    changelog: null,
                    endDateTime : "2023-12-31T09:00:00Z",
                    priority : (classification.toLocaleLowerCase() === "complaint") ? "HIGH" : "LOW",
                    branches : null,
                    salesOrder : null,
                    dueDateTime: "2023-12-31T22:59:00Z",
                    salesQuotation : null,
                    udfMetaGroups : null,
                    orderReference : null,
                    responsibles : [
                            "14523B3D57424338858CB56BBF120696"
                        ],
                    syncStatus : "IN_CLOUD",
                    statusCode : "-2",
                    businessPartner : "8FA7D41CD4C448BF9A27962E9055C141",
                    projectPhase : null,
                    technicians : [],
                    typeName : "Unplanned",
                    chargeableMileages : false,
                    orgLevel : null,
                    chargeableMaterials : false,
                    statusName : "Ready to plan",
                    orderDateTime : null,
                    chargeableExpenses : false,
                    lastChanged : 1544172897151,
                    durationInMinutes : null,
                    serviceContract : null,
                    createPerson : "14523B3D57424338858CB56BBF120696",
                    externalId : null,
                    groups : null,
                    team : null,
                    typeCode : "-1",
                    equipments : [
                            "3B981A0D8206421393DB124C2430F95E"
                        ],
                    startDateTime : "2022-12-09T08:00:00Z",
                    location : null,
                    udfValues : null,
                    incident : null,
                    remarks : null,
                    originName : "Intelligent Ticket System"                    
                };
                const headers = {
                    "X-Client-ID" : "DemoClient",
                    "X-Client-Version" : "1.0",
                    "X-Account-ID" : 96388,
                    "X-Company-ID" : 108432

                };
                const FSM_resp = await FSM.send("POST", "/ServiceCall/?dtos=ServiceCall.26", FSM_payload, headers);
                code = FSM_resp.data[0].serviceCall.code;
            }

            // Configure reply message accourding to route
            const replyMessage = (action === "CRM") ? 'Thank you for reaching out. A service call for your ' + classification.toLocaleLowerCase() + ' with code "' + code + '" has been created in our system. A representative will contact you soon.' : "Thank you for appreciating our service. We hope to keep always satisfying your expectations!";

            // Respond to the requester
            const res = {
                type: classification,
                route: action,
                replyMessage: replyMessage
            };

            return res;
        } catch (err) {
            req.error(err.code, err.message);
        }
    });
});