using TicketingService as service from '../../srv/ticketing-service';

annotate service.InteractionInsight with {
    ID            @ID   : 'ID';
    title         @title: 'Title';
    summary       @title: 'Description';
    createdAt     @title: 'Creation Date';
    priority_code @title: 'Priority';
    status        @title: 'Status';
    category      @title: 'Category';
    impact        @title: 'Impact';
    riskyear      @title: 'Year';
};

annotate service.InteractionInsight with @(
    Common.SemanticKey: [ID],
    UI                : {
        Identification  : [{Value: ID}],
        SelectionFields : [
            ID,
            status_code,
            category_code,
            summary
        ],
        LineItem #list01: [
            {
                $Type            : 'UI.DataField',
                Value            : title,
                ![@UI.Importance]: #High,
            },
            {
                $Type            : 'UI.DataField',
                Value            : summary,
                ![@UI.Importance]: #High,
            },
            {
                $Type            : 'UI.DataField',
                Value            : createdAt,
                ![@UI.Importance]: #High,
            },
            {
                $Type            : 'UI.DataField',
                Value            : priority_code,
                ![@UI.Importance]: #High,
            }
        ]
    }
);

annotate service.InboundCustomerMessage with @(UI: {
    PresentationVariant #chart03: {Visualizations: ['@UI.Chart#chart03', ], },
    Chart #chart03              : {
        ChartType          : #Column,
        Dimensions         : [intent.name],
        DimensionAttributes: [{
            Dimension: intent.name,
            Role     : #Category
        }],
        Measures           : [numberOfInboundCustomerMsgs],
        MeasureAttributes  : [{
            Measure: numberOfInboundCustomerMsgs,
            Role   : #Axis1
        }]
    }
});

annotate service.InteractionInsight with @(UI: {
    PresentationVariant #chart01: {Visualizations: ['@UI.Chart#chart01', ], },
    Chart                       : {
        ChartType          : #Column,
        Dimensions         : [StatusTxt],
        DimensionAttributes: [{
            Dimension: StatusTxt,
            Role     : #Category
        }],
        Measures           : [numberOfInteractions],
        MeasureAttributes  : [{
            Measure: numberOfInteractions,
            Role   : #Axis1
        }]
    },
    Chart #chart01              : {
        ChartType          : #Column,
        Dimensions         : [priority_code],
        DimensionAttributes: [{
            Dimension: priority_code,
            Role     : #Category
        }],
        Measures           : [numberOfInteractions],
        MeasureAttributes  : [{
            Measure: numberOfInteractions,
            Role   : #Axis1
        }]
    },
    HeaderInfo                  : {
        TypeName      : '{i18n>Message}',
        TypeNamePlural: '{i18n>Messages}',
        Title         : {Value: Aedate},
        Description   : {Value: Aedate}
    },
    Facets                      : [{
        $Type : 'UI.ReferenceFacet',
        Label : '{i18n>Details}',
        Target: '@UI.FieldGroup#Details'
    }, ],
    FieldGroup #Details         : {Data: [
        {Value: Pointer},
        {Value: Aedate},
        {Value: Status},
        {Value: StatusTxt},
        {Value: PriorityTxt},
        {Value: numberOfInteractions}

    ]}
});

annotate service.InteractionInsight with @(UI: {
    PresentationVariant #chart02: {Visualizations: ['@UI.Chart#chart02', ], },
    Chart #chart02              : {
        ChartType          : #Donut,
        Dimensions         : [priorname],
        DimensionAttributes: [{
            Dimension: priorname,
            Role     : #Category
        }],
        Measures           : [numberOfInteractions],
        MeasureAttributes  : [{
            Measure: numberOfInteractions,
            Role   : #Axis1
        }]
    }
});

annotate service.InteractionInsight with @(UI: {
    PresentationVariant #chart04: {Visualizations: ['@UI.Chart#chart04', ], },
    Chart #chart04              : {
        ChartType          : #Donut,
        Dimensions         : [catname],
        DimensionAttributes: [{
            Dimension: catname,
            Role     : #Category
        }],
        Measures           : [numberOfInteractions],
        MeasureAttributes  : [{
            Measure: numberOfInteractions,
            Role   : #Axis1
        }]
    }
});

annotate service.InboundCustomerMessage with @(UI: {
    PresentationVariant #chart05: {Visualizations: ['@UI.Chart#chart05', ], },
    Chart #chart05              : {
        ChartType          : #Donut,
        Dimensions         : [sentiment],
        DimensionAttributes: [{
            Dimension: sentiment,
            Role     : #Category
        }],
        Measures           : [numberOfInboundCustomerMsgs],
        MeasureAttributes  : [{
            Measure: numberOfInboundCustomerMsgs,
            Role   : #Axis1
        }]
    }
});

annotate service.InteractionInsight with @(UI: {
    PresentationVariant #chart05: {Visualizations: ['@UI.Chart#chart05', ], },
    Chart #chart05              : {
        ChartType          : #Bar,
        Dimensions         : [customer_ID],
        DimensionAttributes: [{
            Dimension: customer_ID,
            Role     : #Category
        }],
        Measures           : [numberOfInteractions],
        MeasureAttributes  : [{
            Measure: numberOfInteractions,
            Role   : #Axis1
        }]
    }
});

annotate service.InteractionInsight with @(UI: {
    PresentationVariant #chart06: {Visualizations: ['@UI.Chart#chart06', ], },
    Chart #chart06              : {
        ChartType          : #Bar,
        Dimensions         : [customer_ID],
        DimensionAttributes: [{
            Dimension: customer_ID,
            Role     : #Category
        }],
        Measures           : [numberOfInteractions],
        MeasureAttributes  : [{
            Measure: numberOfInteractions,
            Role   : #Axis1
        }]
    },
    DataPoint #chart06          : {
        $Type                 : 'UI.DataPointType',
        Title                 : 'KPI Card',
        Value                 : numberOfInteractions,
        ValueFormat           : {
            ScaleFactor             : 2,
            NumberOfFractionalDigits: 1
        },
        CriticalityCalculation: {
            ImprovementDirection   : #Minimizing,
            DeviationRangeHighValue: '7300',
            ToleranceRangeHighValue: '7200'
        },
        TargetValue           : '2.000 ',
        TrendCalculation      : {
            ReferenceValue: '5201680',
            DownDifference: 10000000.0
        }
    },
    KPI #chart06                : {
        $Type           : 'UI.KPIType',
        Detail          : {
            $Type                     : 'UI.KPIDetailType',
            DefaultPresentationVariant: ![@UI.PresentationVariant#chart06],
            SemanticObject            : 'Action',
            Action                    : 'toappnavsample'
        },
        SelectionVariant: ![@UI.SelectionVariant#chart06],
        DataPoint       : ![@UI.DataPoint#chart06],
        ID              : 'String for KPI Annotation'
    },
    PresentationVariant #chart06: {
        MaxItems : 5,
        GroupBy  : [category_code],
        SortOrder: [{
            Property  : ID,
            Descending: true
        }, ]
    },
    SelectionVariant #chart06   : {
        SelectOptions: [{
            PropertyName: category_code,
            Ranges      : [{
                Sign  : #I,
                Option: #EQ,
                Low   : 'PRD'
            }]
        }],
        Parameters   : [
            {
                $Type        : 'UI.Parameter',
                PropertyName : status_code,
                PropertyValue: 'NW'
            },
            {
                $Type        : 'UI.Parameter',
                PropertyName : priority_code,
                PropertyValue: 'H'
            }
        ]
    }

});

annotate service.InteractionInsight with @(UI: {
    PresentationVariant #chart07: {Visualizations: ['@UI.Chart#chart07', ], },
    Chart #chart07              : {
        ChartType          : #Line,
        Dimensions         : [customer_ID],
        DimensionAttributes: [{
            Dimension: customer_ID,
            Role     : #Category
        }],
        Measures           : [numberOfInteractions],
        MeasureAttributes  : [{
            Measure: numberOfInteractions,
            Role   : #Axis1
        }]
    }
});
