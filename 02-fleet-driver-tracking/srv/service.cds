using {fdt_app.db as db} from '../db/schema';

@path     : 'fdt/service'
@requires : 'authenticated-user'
service FDTAppService {
    entity Employee     as projection on db.Employee;
    entity Vehicle      as projection on db.Vehicle;
    entity VehicleDrive as projection on db.VehicleDrive;
    entity DriveHistory as projection on db.DriveHistory;

    annotate Employee with {
        userId          @(
            Common : {
                Label : 'ID',
                Text  : {
                    $value                 : defaultFullName,
                    ![@UI.TextArrangement] : #TextOnly,
                }
            },
            UI     : {Hidden : true}
        );
        defaultFullName @(Common : {Label : 'Name'});
        department      @(Common : {Label : 'Department'});
        division        @(Common : {Label : 'Division'});
        email           @(Common : {Label : 'e-Mail'});
        firstName       @(Common : {Label : 'First Name'});
        lastName        @(Common : {Label : 'Last Name'});
        title           @(Common : {Label : 'Title'});
    };

    annotate Employee @(Capabilities : {
        SearchRestrictions : {
            $Type      : 'Capabilities.SearchRestrictionsType',
            Searchable : false
        },
        Insertable         : false,
        Deletable          : false,
        Updatable          : false
    });

    annotate Employee with @(UI : {
        UpdateHidden   : true,
        DeleteHidden   : true,
        CreateHidden   : true,
        Identification : [{Value : defaultFullName}]
    });

    annotate Employee with @(UI.LineItem : [
        {
            $Type : 'UI.DataField',
            Value : defaultFullName
        },
        {
            $Type : 'UI.DataField',
            Value : title
        },
        {
            $Type : 'UI.DataField',
            Value : email
        },
        {
            $Type : 'UI.DataField',
            Value : division
        },
        {
            $Type : 'UI.DataField',
            Value : department
        }
    ]);

    annotate Employee with @(UI.HeaderInfo : {
        TypeName       : 'Driver',
        TypeNamePlural : 'Drivers',
        Title          : {
            $Type : 'UI.DataField',
            Value : defaultFullName,
        },
        Description    : {
            $Type : 'UI.DataField',
            Value : title,
        }
    });

    annotate Employee with @(
        UI.FieldGroup #General : {
            $Type : 'UI.FieldGroupType',
            Data  : [
                {
                    $Type : 'UI.DataField',
                    Value : email
                },
                {
                    $Type : 'UI.DataField',
                    Value : division
                },
                {
                    $Type : 'UI.DataField',
                    Value : department
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
                ID     : 'History',
                Label  : 'Drive History',
                Target : 'history/@UI.LineItem#History',
            }
        ]
    );

    annotate Employee with @(UI.SelectionFields : [
        firstName,
        lastName
    ]);

    annotate Vehicle with {
        company      @(
            Common : {Label : 'Company'},
            UI     : {Hidden : true}
        );
        code         @(
            Common : {
                Label : 'Code',
                Text  : {
                    $value                 : name,
                    ![@UI.TextArrangement] : #TextOnly,
                }
            },
            UI     : {Hidden : true}
        );
        asset        @(
            Common : {Label : 'Asset'},
            UI     : {Hidden : true}
        );
        name         @(Common : {Label : 'Vehicle'});
        className    @(Common : {Label : 'Category'});
        licensePlate @(Common : {Label : 'License Plate'});
    };

    annotate Vehicle with @(UI : {
        UpdateHidden   : true,
        DeleteHidden   : true,
        CreateHidden   : true,
        Identification : [{Value : name}]
    });

    annotate Vehicle @(Capabilities : {
        SearchRestrictions : {
            $Type      : 'Capabilities.SearchRestrictionsType',
            Searchable : true
        },
        Insertable         : false,
        Deletable          : false,
        Updatable          : false
    });

    annotate Vehicle with @(UI.LineItem : [
        {
            $Type : 'UI.DataField',
            Value : name
        },
        {
            $Type : 'UI.DataField',
            Value : className
        },
        {
            $Type : 'UI.DataField',
            Value : licensePlate
        }
    ]);

    annotate Vehicle with @(UI.HeaderInfo : {
        TypeName       : 'Vehicle',
        TypeNamePlural : 'Vehicles',
        Title          : {
            $Type : 'UI.DataField',
            Value : name,
        },
        Description    : {
            $Type : 'UI.DataField',
            Value : licensePlate,
        }
    });

    annotate Vehicle with @(
        UI.FieldGroup #General : {
            $Type : 'UI.FieldGroupType',
            Data  : [
                {
                    $Type : 'UI.DataField',
                    Value : className
                },
                {
                    $Type : 'UI.DataField',
                    Value : name
                },
                {
                    $Type : 'UI.DataField',
                    Value : licensePlate
                }
            ],
        },
        UI.Facets              : [{
            $Type  : 'UI.ReferenceFacet',
            ID     : 'General',
            Label  : 'General',
            Target : '@UI.FieldGroup#General',
        }]
    );

    annotate Vehicle with @(UI.SelectionFields : [
        name,
        licensePlate
    ]);

    annotate VehicleDrive with {
        code         @(Common : {Label : 'Code'});
        name         @(Common : {Label : 'Vehicle'});
        licensePlate @(Common : {Label : 'License Plate'});
    };

    annotate VehicleDrive with @(UI : {
        UpdateHidden   : true,
        DeleteHidden   : true,
        CreateHidden   : true,
        Identification : [{Value : name}]
    });

    annotate VehicleDrive @(Capabilities : {
        SearchRestrictions : {
            $Type      : 'Capabilities.SearchRestrictionsType',
            Searchable : true
        },
        Insertable         : false,
        Deletable          : false,
        Updatable          : false
    });

    annotate VehicleDrive with @(UI.LineItem : [
        {
            $Type : 'UI.DataField',
            Value : code
        },
        {
            $Type : 'UI.DataField',
            Value : name
        },
        {
            $Type : 'UI.DataField',
            Value : licensePlate
        }
    ]);

    annotate VehicleDrive with @(UI.HeaderInfo : {
        TypeName       : 'Vehicle',
        TypeNamePlural : 'Vehicles',
        Title          : {
            $Type : 'UI.DataField',
            Value : name,
        },
        Description    : {
            $Type : 'UI.DataField',
            Value : licensePlate,
        }
    });

    annotate VehicleDrive with @(UI.SelectionFields : [
        name,
        licensePlate
    ]);

    annotate DriveHistory with {
        driver                          @(Common : {
            Label                    : 'Driver',
            Text                     : {
                $value                 : driver.defaultFullName,
                ![@UI.TextArrangement] : #TextOnly,
            },
            ValueList                : {
                $Type          : 'Common.ValueListType',
                CollectionPath : 'Employee',
                Parameters     : [
                    {
                        $Type             : 'Common.ValueListParameterInOut',
                        LocalDataProperty : driver_userId,
                        ValueListProperty : 'userId',
                    },
                    {
                        $Type             : 'Common.ValueListParameterDisplayOnly',
                        ValueListProperty : 'defaultFullName',
                    },
                    {
                        $Type             : 'Common.ValueListParameterDisplayOnly',
                        ValueListProperty : 'email',
                    },
                ]
            },
            ValueListWithFixedValues : false
        });
        startDateTime                   @(Common : {Label : 'Start'});
        endDateTime                     @(Common : {Label : 'End'});
        vehicle                         @(
            Common : {
                Label                    : 'Vehicle',
                Text                     : {
                    $value                 : vehicle.name,
                    ![@UI.TextArrangement] : #TextOnly,
                },
                ValueList                : {
                    $Type          : 'Common.ValueListType',
                    CollectionPath : 'Vehicle',
                    Parameters     : [
                        {
                            $Type             : 'Common.ValueListParameterInOut',
                            LocalDataProperty : vehicle_code,
                            ValueListProperty : 'code',
                        },
                        {
                            $Type             : 'Common.ValueListParameterDisplayOnly',
                            ValueListProperty : 'name',
                        },
                        {
                            $Type             : 'Common.ValueListParameterDisplayOnly',
                            ValueListProperty : 'licensePlate',
                        }                    ]
                },
                ValueListWithFixedValues : false
            },
            UI     : {Hidden : false}
        );
        distance                        @(Common : {Label : 'Distance'});
        fuelConsumption                 @(Common : {Label : 'Fuel Consumption'});
        maxRPM                          @(Common : {Label : 'Max. RPM'});
        maxSpeed                        @(Common : {Label : 'Max. Speed'});
        nbHarshBraking                  @(Common : {Label : '# Harsh Brakings'});
        nbHarshCornering                @(Common : {Label : '# Harsh Cornering'});
        nbRapidAcceleration             @(Common : {Label : '# Rapid Accelerations'});
        nbTailGating                    @(Common : {Label : '# Tail Gatings'});
        nbInfoTainmentUsageWhileDriving @(Common : {Label : '# InfoTainment While Driving'});
    };

    annotate DriveHistory @(Capabilities : {
        SearchRestrictions : {
            $Type      : 'Capabilities.SearchRestrictionsType',
            Searchable : false
        },
        Insertable         : false,
        Deletable          : false,
        Updatable          : false
    });

    annotate DriveHistory with @(UI : {
        UpdateHidden   : true,
        DeleteHidden   : true,
        CreateHidden   : true,
        Identification : [{Value : driver_userId}]
    });

    annotate DriveHistory with @(UI.LineItem : [
        {
            $Type : 'UI.DataField',
            Value : startDateTime
        },
        {
            $Type : 'UI.DataField',
            Value : endDateTime
        },
        {
            $Type : 'UI.DataField',
            Value : vehicle_code
        },
        {
            $Type : 'UI.DataField',
            Value : vehicle.licensePlate
        },
        {
            $Type : 'UI.DataField',
            Value : distance
        }
    ]);

    annotate DriveHistory with @(UI.LineItem #History : [
        {
            $Type : 'UI.DataField',
            Value : startDateTime
        },
        {
            $Type : 'UI.DataField',
            Value : endDateTime
        },
        {
            $Type : 'UI.DataField',
            Value : vehicle_code
        },
        {
            $Type : 'UI.DataField',
            Value : vehicle.licensePlate
        },
        {
            $Type : 'UI.DataField',
            Value : distance
        },
        {
            $Type : 'UI.DataField',
            Value : fuelConsumption
        },
        {
            $Type : 'UI.DataField',
            Value : maxRPM
        },
        {
            $Type : 'UI.DataField',
            Value : maxSpeed
        }
    ]);

    annotate DriveHistory with @(UI.HeaderInfo : {
        TypeName       : 'History',
        TypeNamePlural : 'History',
        Title          : {
            $Type : 'UI.DataField',
            Value : driver_userId
        },
        Description    : {
            $Type : 'UI.DataField',
            Value : vehicle_code
        }
    });

    annotate DriveHistory with @(
        UI.FieldGroup #General : {
            $Type : 'UI.FieldGroupType',
            Data  : [
                {
                    $Type : 'UI.DataField',
                    Value : startDateTime
                },
                {
                    $Type : 'UI.DataField',
                    Value : endDateTime
                },
                {
                    $Type : 'UI.DataField',
                    Value : vehicle.licensePlate
                },
                {
                    $Type : 'UI.DataField',
                    Value : endDateTime
                },
                {
                    $Type : 'UI.DataField',
                    Value : distance
                },
                {
                    $Type : 'UI.DataField',
                    Value : fuelConsumption
                },
                {
                    $Type : 'UI.DataField',
                    Value : maxRPM
                },
                {
                    $Type : 'UI.DataField',
                    Value : nbHarshBraking
                },
                {
                    $Type : 'UI.DataField',
                    Value : nbHarshCornering
                },
                {
                    $Type : 'UI.DataField',
                    Value : nbRapidAcceleration
                },
                {
                    $Type : 'UI.DataField',
                    Value : nbTailGating
                },
                {
                    $Type : 'UI.DataField',
                    Value : nbInfoTainmentUsageWhileDriving
                }
            ],
        },
        UI.Facets              : [{
            $Type  : 'UI.ReferenceFacet',
            ID     : 'General',
            Label  : 'General',
            Target : '@UI.FieldGroup#General',
        }]
    );

    annotate DriveHistory with @(UI.SelectionFields : [
        vehicle_code,
        startDateTime,
        endDateTime
    ]);
}
