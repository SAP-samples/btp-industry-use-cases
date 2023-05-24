using {cuid} from '@sap/cds/common';

namespace wpm.db;

entity Workspace {
    key irn        : String(80);
        shortName  : String(20);
        longName   : String(100);
        type       : String(15);
        workPlaces : Composition of many Workplace
                         on workPlaces.space = $self;
}

entity Workplace {
    key irn        : String(80);
        space      : Association to Workspace;
        space_name : String(100);
        name       : String(50);
        bookings   : Composition of many Booking
                         on bookings.place = $self;
}

@readonly
entity WorkspaceType {
    key type : String(15);
};

entity Booking : cuid {
    fromDateTime : DateTime;
    toDateTime   : DateTime;
    userId       : String(150);
    space        : Association to Workspace;
    place        : Association to Workplace;
    virtual deletable    : Boolean default false;
    virtual updateHidden : Boolean default true;
};
