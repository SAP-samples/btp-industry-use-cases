using TicketingService as service from '../../srv/ticketing-service';

annotate service.OutboundServiceMessageType with @(
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
    ]
);
annotate service.OutboundServiceMessageType with @(
    UI.FieldGroup #GeneratedGroup1 : {
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
        ],
    },
    UI.Facets : [
        {
            $Type : 'UI.ReferenceFacet',
            ID : 'GeneratedFacet1',
            Label : 'General Information',
            Target : '@UI.FieldGroup#GeneratedGroup1',
        },
    ]
);
