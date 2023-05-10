using AdminService as service from '../../srv/admin-service';

annotate service.CustomerInteraction with @(
    Common.SemanticKey : [ID],
    UI                 : {
        Identification  : [{Value : ID}],
        SelectionFields : [
            ID,
            status_code,
            category_code,
            summary
        ],
        LineItem : [
        {
            $Type : 'UI.DataField',
            Label : '{i18n>ID}',
            Value : ID,
        },
        {
            $Type : 'UI.DataField',
            Label : '{i18n>extRef}',
            Value : extRef,
        },
        {
            $Type : 'UI.DataField',
            Label : '{i18n>category_code}',
            Value : category_code,
        },
        {
            $Type : 'UI.DataField',
            Label : '{i18n>originChannel_code}',
            Value : originChannel_code,
        },
        {
            $Type : 'UI.DataField',
            Label : '{i18n>status_code}',
            Value : status_code,
        },
    ]
    }
) {
    ID @Common : {
        SemanticObject  : 'CustomerInteraction',
        Text            : title,
        TextArrangement : #TextOnly
    };
};

annotate service.CustomerInteraction with @(
    UI.FieldGroup #General : {
        $Type : 'UI.FieldGroupType',
        Data : [
            {
                $Type : 'UI.DataField',
                Label : '{i18n>ID}',
                Value : ID,
            },
            {
                $Type : 'UI.DataField',
                Label : '{i18n>extRef}',
                Value : extRef,
            },
            {
                $Type : 'UI.DataField',
                Label : '{i18n>category}',
                Value : category.name,
            },
            {
                $Type : 'UI.DataField',
                Label : '{i18n>channel}',
                Value : originChannel.name,
            },
            {
                $Type : 'UI.DataField',
                Label : '{i18n>status}',
                Value : status.name,
            },
            {
                $Type : 'UI.DataField',
                Label : '{i18n>priority}',
                Value : priority.name,
            },
            {
                $Type : 'UI.DataField',
                Label : '{i18n>title}',
                Value : title,
            },
            {
                $Type : 'UI.DataField',
                Label : '{i18n>summary}',
                Value : summary,
            },
            {
                $Type : 'UI.DataField',
                Label : '{i18n>tags}',
                Value : tags,
            },
        ],
    },
    UI.Facets : [
        {
            $Type : 'UI.ReferenceFacet',
            ID : 'GeneralFacet',
            Label : '{i18n>General}',
            Target : '@UI.FieldGroup#General',
        },
    ]
);
