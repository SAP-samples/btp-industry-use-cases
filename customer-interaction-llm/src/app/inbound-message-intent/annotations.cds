using AdminService as service from '../../srv/admin-service';

annotate service.InboundCustomerMessageTopic with @(
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
        },
        {
            $Type : 'UI.DataField',
            Label : '{i18n>embedding}',
            Value : embedding,
        },
    ]
);
annotate service.InboundCustomerMessageTopic with @(
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
            {
                $Type : 'UI.DataField',
                Label : '{i18n>descr}',
                Value : descr,
            },
            {
                $Type : 'UI.DataField',
                Label : '{i18n>embedding}',
                Value : embedding,
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
