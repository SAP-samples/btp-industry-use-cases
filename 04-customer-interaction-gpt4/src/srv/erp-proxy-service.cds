service ErpProxyService @(path : '/erp-proxy') {

    //type defintion for the final result of an process result of a customer text message
    type CustomerMsgReturnType {
        created_at: Integer;
        total_tokens   : Integer;
    };

    /**
     * A generic API to invoke LLM API and turn it into your custom REST API
     * Output as JSON
     */
    action checkDeliveryStatus(orderNo : String) returns CustomerMsgReturnType;

    action createSupportTicket();
}