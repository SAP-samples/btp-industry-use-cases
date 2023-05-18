using AdminService as service from '../../srv/admin-service';

annotate service.InteractionInsight with {
    ID          @ID: 'ID';
	title       @title: 'Title';
	summary       @title: 'Description';
    createdAt   @title: 'Creation Date';
    priority_code    @title: 'Priority';
	impact      @title: 'Impact';
    riskyear    @title: 'Year';
};

annotate service.InteractionInsight with @(
    UI.LineItem : {
        $value : [
            {
                $Type               : 'UI.DataField',
                Value               : title,
                ![@UI.Importance]   : #High,
            },
            {
                $Type               : 'UI.DataField',
                Value               : summary,
                ![@UI.Importance]   : #High,
            },
            {
                $Type               : 'UI.DataField',
                Value               : createdAt,
                ![@UI.Importance]   : #High,
            },
            {
                $Type               : 'UI.DataField',
                Value               : priority_code,
                ![@UI.Importance]   : #High,
            },
        ],
    },
);