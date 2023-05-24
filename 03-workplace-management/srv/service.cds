using wpm.db as db from '../db/schema';

namespace wpm.srv;

@path : 'wpm/service'
@requires : 'Employee'
service WPMService {
    entity Workspace     as projection on db.Workspace;

    entity Workplace     as projection on db.Workplace actions {
        @cds.odata.bindingparameter.collection
        action refreshData() returns Boolean;
    };

    entity WorkspaceType as projection on db.WorkspaceType;
    entity Booking       as projection on db.Booking;

    annotate Workspace with {
        irn        @(
            Common : {
                Label : 'ID',
                Text  : {
                    $value                 : longName,
                    ![@UI.TextArrangement] : #TextOnly,
                }
            },
            UI     : {Hidden : true}
        )                                             @readonly;
        shortName  @(Common : {Label : 'Code'})       @readonly;
        longName   @(Common : {Label : 'Workspace'})  @readonly;
        type       @(Common : {
            Label     : 'Type',
            ValueListWithFixedValues,
            ValueList : {
                $Type          : 'Common.ValueListType',
                CollectionPath : 'WorkspaceType',
                Parameters     : [
                    {
                        $Type             : 'Common.ValueListParameterInOut',
                        LocalDataProperty : 'type',
                        ValueListProperty : 'type'
                    },
                    {
                        $Type             : 'Common.ValueListParameterDisplayOnly',
                        ValueListProperty : 'type'
                    }
                ]
            }
        })                                            @readonly;
    };

    annotate Workspace @(Capabilities : {
        SearchRestrictions : {
            $Type      : 'Capabilities.SearchRestrictionsType',
            Searchable : true
        },
        Insertable         : false,
        Deletable          : false,
        Updatable          : false
    });

    annotate Workspace with @(UI : {
        UpdateHidden   : true,
        DeleteHidden   : true,
        CreateHidden   : true,
        Identification : [{Value : shortName}]
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
        longName,
        type
    ]);

    annotate Workplace with @odata.draft.enabled;

    annotate Workplace with {
        irn         @(
            Common : {
                Label : 'ID',
                Text  : {
                    $value                 : name,
                    ![@UI.TextArrangement] : #TextOnly,
                }
            },
            UI     : {Hidden : true}
        )                                              @readonly;
        space       @(Common : {
            Label     : 'Workspace',
            Text      : {
                $value                 : space_name,
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
        })                                             @readonly;
        space_name  @(
            Common : {Label : 'Workspace'},
            UI     : {Hidden : true}
        )                                              @readonly;
        name        @(Common : {Label : 'Workplace'})  @readonly;
    };

    annotate Workplace @(Capabilities : {
        SearchRestrictions : {
            $Type      : 'Capabilities.SearchRestrictionsType',
            Searchable : true
        },
        Insertable         : false,
        Deletable          : false,
        Updatable          : true
    });

    annotate Workplace with @(UI : {
        UpdateHidden        : false,
        DeleteHidden        : true,
        CreateHidden        : true,
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
        },
        {
            $Type              : 'UI.DataFieldForAction',
            Label              : 'Refresh',
            Action             : 'wpm.srv.WPMService.refreshData',
            InvocationGrouping : #Isolated
        }
    ]);

    annotate Workplace with actions {
        refreshData @(
            cds.odata.bindingparameter.name : '_it',
            Core.OperationAvailable         : true,
            Common                          : {
                IsActionCritical : false,
                SideEffects      : {
                    $Type          : 'Common.SideEffectsType',
                    TargetEntities : ['_it']
                }
            }
        )
    };

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
        UI.Facets              : [
            {
                $Type  : 'UI.ReferenceFacet',
                ID     : 'General',
                Label  : 'General',
                Target : '@UI.FieldGroup#General'
            },
            {
                $Type  : 'UI.ReferenceFacet',
                ID     : 'Bookings',
                Label  : 'Bookings',
                Target : 'bookings/@UI.LineItem#Bookings'
            }
        ]
    );

    annotate Workplace with @(UI.SelectionFields : [
        space_irn,
        name
    ]);

    annotate Booking with {
        ID     @(UI : {Hidden : true});
        space  @(
            Common : {
                Label        : 'Workspace',
                FieldControl : #Mandatory,
                Text         : {
                    $value                 : space.longName,
                    ![@UI.TextArrangement] : #TextOnly
                },
                ValueListWithFixedValues,
                ValueList    : {
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
            },
            UI     : {Hidden : true}
        )                                    @readonly;
        place  @(
            Common : {
                Label        : 'Workplace',
                FieldControl : #Mandatory,
                Text         : {
                    $value                 : place.name,
                    ![@UI.TextArrangement] : #TextOnly
                },
                ValueListWithFixedValues,
                ValueList    : {
                    $Type          : 'Common.ValueListType',
                    CollectionPath : 'Workplace',
                    Parameters     : [
                        {
                            $Type             : 'Common.ValueListParameterOut',
                            LocalDataProperty : 'place_irn',
                            ValueListProperty : 'irn'
                        },
                        {
                            $Type             : 'Common.ValueListParameterIn',
                            LocalDataProperty : 'space_irn',
                            ValueListProperty : 'space_irn'
                        },
                        {
                            $Type             : 'Common.ValueListParameterDisplayOnly',
                            ValueListProperty : 'name'
                        }
                    ]
                }
            },
            UI     : {Hidden : true}
        )                                    @readonly;
        fromDateTime

               @(Common : {
            Label        : 'From',
            FieldControl : #Mandatory
        });
        toDateTime

               @(Common : {
            Label        : 'To',
            FieldControl : #Mandatory
        });
        userId

               @(Common : {Label : 'User'})  @readonly;
        deletable

               @(
            Common    : {Label : 'Deletable'},
            UI.Hidden : true
        )                                    @readonly;
        updateHidden

               @(
            Common    : {Label : 'Update Hidden'},
            UI.Hidden : true
        )                                    @readonly;
    };

    annotate Booking @(Capabilities : {
        SearchRestrictions : {
            $Type      : 'Capabilities.SearchRestrictionsType',
            Searchable : true
        },
        Insertable         : true,
        DeleteRestrictions : {
            $Type     : 'Capabilities.DeleteRestrictionsType',
            Deletable : deletable
        },
        UpdateRestrictions : {
            $Type     : 'Capabilities.UpdateRestrictionsType',
            Updatable : deletable
        }
    });

    annotate Booking with @(UI : {
        UpdateHidden        : updateHidden,
        DeleteHidden        : false,
        CreateHidden        : false,
        Identification      : [{Value : place_irn}],
        PresentationVariant : {
            SortOrder      : [
                {
                    Property   : space_irn,
                    Descending : false,
                },
                {
                    Property   : place_irn,
                    Descending : false,
                },
                {
                    Property   : fromDateTime,
                    Descending : false,
                },
                {
                    Property   : toDateTime,
                    Descending : false,
                }
            ],
            Visualizations : [
                '@UI.LineItem',
                '@UI.LineItem#Bookings'
            ],
        }
    });

    annotate Booking with @(UI.LineItem : [
        {
            $Type : 'UI.DataField',
            Value : place.space_name
        },
        {
            $Type : 'UI.DataField',
            Value : place_irn
        },
        {
            $Type : 'UI.DataField',
            Value : fromDateTime
        },
        {
            $Type : 'UI.DataField',
            Value : toDateTime
        },
        {
            $Type : 'UI.DataField',
            Value : userId
        }
    ]);

    annotate Booking with @(UI.LineItem #Bookings : [
        {
            $Type : 'UI.DataField',
            Value : fromDateTime
        },
        {
            $Type : 'UI.DataField',
            Value : toDateTime
        },
        {
            $Type : 'UI.DataField',
            Value : userId
        }
    ]);

    annotate Booking with @(UI.HeaderInfo : {
        TypeName       : 'Booking',
        TypeNamePlural : 'Bookings',
        Title          : {
            $Type : 'UI.DataField',
            Value : space_irn
        },
        Description    : {
            $Type : 'UI.DataField',
            Value : place_irn
        }
    });

    annotate Booking with @(
        UI.FieldGroup #General : {
            $Type : 'UI.FieldGroupType',
            Data  : [
                {
                    $Type : 'UI.DataField',
                    Value : fromDateTime
                },
                {
                    $Type : 'UI.DataField',
                    Value : toDateTime
                },
                {
                    $Type : 'UI.DataField',
                    Value : userId
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

    annotate Booking with @(UI.SelectionFields : [
        space_irn,
        place_irn,
        fromDateTime,
        toDateTime,
        userId
    ]);
}
