using wpm.db as db from '../db/schema';

namespace wpm.srv;

@path : 'wpm/admin'
@requires : 'FacilitiesManager'
service WPMAdmin {
    entity Workspace as projection on db.Workspace
    entity Workplace as projection on db.Workplace;
    annotate Workspace with @odata.draft.enabled;

    annotate Workspace with {
        irn       @(
            Common : {
                Label : 'Internal ID',
                Text  : {
                    $value                 : shortName,
                    ![@UI.TextArrangement] : #TextOnly,
                }
            },
            UI.Hidden
        );
        shortName @(Common : {
            Label        : 'Code',
            FieldControl : #Mandatory
        });
        longName  @(Common : {
            Label        : 'Workspace',
            FieldControl : #Mandatory
        });
        type      @(Common : {Label : 'Type'})  @readonly;
    }

    annotate Workspace @(Capabilities : {
        SearchRestrictions : {
            $Type      : 'Capabilities.SearchRestrictionsType',
            Searchable : true
        },
        Insertable         : true,
        Deletable          : true,
        Updatable          : true
    });

    annotate Workspace with @(UI : {
        UpdateHidden   : false,
        DeleteHidden   : false,
        CreateHidden   : false,
        Identification : [{Value : shortName}],
        PresentationVariant : {
            SortOrder      : [
                {
                    Property   : longName,
                    Descending : false,
                }
            ],
            Visualizations : [
                '@UI.LineItem'
            ]
        }
    });

    annotate Workspace with @(UI.LineItem : [
        {
            $Type : 'UI.DataField',
            Value : shortName
        },
        {
            $Type : 'UI.DataField',
            Value : longName
        },
        {
            $Type : 'UI.DataField',
            Value : type
        }
    ]);

    annotate Workspace with @(UI.HeaderInfo : {
        TypeName       : 'Workspace',
        TypeNamePlural : 'Workspaces',
        Title          : {
            $Type : 'UI.DataField',
            Value : shortName,
        },
        Description    : {
            $Type : 'UI.DataField',
            Value : longName,
        }
    });

    annotate Workspace with @(
        UI.FieldGroup #General : {
            $Type : 'UI.FieldGroupType',
            Data  : [
                {
                    $Type : 'UI.DataField',
                    Value : shortName
                },
                {
                    $Type : 'UI.DataField',
                    Value : longName
                },
                {
                    $Type : 'UI.DataField',
                    Value : type
                }
            ],
        },
        UI.Facets              : [
            {
                $Type  : 'UI.ReferenceFacet',
                ID     : 'General',
                Label  : 'General',
                Target : '@UI.FieldGroup#General'
            },
            {
                $Type  : 'UI.ReferenceFacet',
                ID     : 'Workplaces',
                Label  : 'Workplaces',
                Target : 'workPlaces/@UI.LineItem#Workplaces',
            }
        ]
    );

    annotate Workspace with @(UI.SelectionFields : [
        shortName,
        longName
    ]);

    annotate Workplace with {
        irn         @(
            Common : {
                Label : 'Internal ID',
                Text  : {
                    $value                 : name,
                    ![@UI.TextArrangement] : #TextOnly,
                }
            },
            UI.Hidden
        );
        space       @(Common : {
            Label     : 'Workspace',
            Text      : {
                $value                 : space.longName,
                ![@UI.TextArrangement] : #TextOnly
            },
            ValueListWithFixedValues,
            ValueList : {
                $Type          : 'Common.ValueListType',
                CollectionPath : 'Workspace',
                Parameters     : [
                    {
                        $Type             : 'Common.ValueListParameterInOut',
                        LocalDataProperty : 'space_irn',
                        ValueListProperty : 'irn'
                    },
                    {
                        $Type             : 'Common.ValueListParameterDisplayOnly',
                        ValueListProperty : 'longName'
                    }
                ]
            }
        });
        space_name  @(
            Common : {Label : 'Workspace'},
            UI     : {Hidden : true}
        )  @readonly;
        name        @(Common : {
            Label        : 'Workplace',
            FieldControl : #Mandatory
        });
    };

    annotate Workplace @(Capabilities : {
        SearchRestrictions : {
            $Type      : 'Capabilities.SearchRestrictionsType',
            Searchable : true
        },
        Insertable         : true,
        Deletable          : true,
        Updatable          : true
    });

    annotate Workplace with @(UI : {
        UpdateHidden        : false,
        DeleteHidden        : false,
        CreateHidden        : false,
        Identification      : [{Value : name}],
        PresentationVariant : {
            SortOrder      : [
                {
                    Property   : space_name,
                    Descending : false,
                },
                {
                    Property   : name,
                    Descending : false,
                }
            ],
            GroupBy        : [space_name],
            Visualizations : [
                '@UI.LineItem',
                '@UI.LineItem#Workplaces'
            ],
        }
    });

    annotate Workplace with @(UI.LineItem : [
        {
            $Type : 'UI.DataField',
            Value : space_irn
        },
        {
            $Type : 'UI.DataField',
            Value : name
        }
    ]);

    annotate Workplace with @(UI.LineItem #Workplaces : [{
        $Type : 'UI.DataField',
        Value : name
    }]);

    annotate Workplace with @(UI.HeaderInfo : {
        TypeName       : 'Workplace',
        TypeNamePlural : 'Workplaces',
        Title          : {
            $Type : 'UI.DataField',
            Value : space_irn,
        },
        Description    : {
            $Type : 'UI.DataField',
            Value : name,
        }
    });

    annotate Workplace with @(
        UI.FieldGroup #General : {
            $Type : 'UI.FieldGroupType',
            Data  : [
                {
                    $Type : 'UI.DataField',
                    Value : space_irn
                },
                {
                    $Type : 'UI.DataField',
                    Value : name
                }
            ]
        },
        UI.Facets              : [{
            $Type  : 'UI.ReferenceFacet',
            ID     : 'General',
            Label  : 'General',
            Target : '@UI.FieldGroup#General'
        }]
    );

    annotate Workplace with @(UI.SelectionFields : [
        space_irn,
        name
    ]);
}
