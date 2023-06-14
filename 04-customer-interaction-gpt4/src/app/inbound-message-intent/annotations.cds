using TicketingService as service from '../../srv/ticketing-service';

annotate service.InboundCustomerMessageIntent with @(
    UI.LineItem : [
        {
            $Type : 'UI.DataField',
            Label : '{i18n>code}',
            Value : code,
        },
        {
            $Type : 'UI.DataField',
            Label : '{i18n>name}',
            Value : name,
        },
        {
            $Type : 'UI.DataField',
            Label : '{i18n>descr}',
            Value : descr,
        }
    ]
);
annotate service.InboundCustomerMessageIntent with @(
    UI.FieldGroup #GeneralGroup : {
        $Type : 'UI.FieldGroupType',
        Data : [
            {
                $Type : 'UI.DataField',
                Label : '{i18n>code}',
                Value : code,
            },
            {
                $Type : 'UI.DataField',
                Label : '{i18n>name}',
                Value : name,
            },
            {
                $Type : 'UI.DataField',
                Label : '{i18n>descr}',
                Value : descr,
            }
        ],
    },
    UI.FieldGroup #EmbeddingGroup : {
        $Type : 'UI.FieldGroupType',
        Data : [
            {
                $Type : 'UI.DataField',
                Value : embedding,
            }
        ],
    },
    UI.Facets : [
        {
            $Type : 'UI.ReferenceFacet',
            ID : 'GeneralFacet',
            Label : '{i18n>General}',
            Target : '@UI.FieldGroup#GeneralGroup',
        },
        {
            $Type : 'UI.ReferenceFacet',
            ID : 'EmbeddingFacet',
            Label : '{i18n>embedding}',
            Target : '@UI.FieldGroup#EmbeddingGroup',
        },
    ]
);

////////////////////////////////////////////////////////////
//
//  Draft for Localized Data
//

annotate xxx.cust.int.llm.InboundCustomerMessageIntent with @fiori.draft.enabled;
annotate TicketingService.InboundCustomerMessageIntent with @odata.draft.enabled;