const cds = require('@sap/cds');
const { randomUUID } = require('crypto');

/*** MODULE INITIALIZATION ***/

let C4RE = null;

(async function () {
    // Connect to external services
    C4RE = await cds.connect.to('C4RE');
})();

/*** GLOBAL CONSTANTS ***/

const db_namespace = 'wpm.db.';

/*** CONTROL FLAGS ***/

var firstRead = true;

/*** HELPERS ***/

// Do the appropriate updates on workspaces
async function refreshWorkspaces(workspaces, req) {
    // Get all current workspaces
    let current = await cds.tx(req).run(SELECT.from(db_namespace + 'Workspace').columns(['irn']).where({ type: 'Owned' }));
    current = (current.length === undefined) ? [current] : current;

    // Added and/or updated workspaces
    const toAdd = [];
    const toUpdate = [];
    workspaces.forEach(entry => {
        const ws = current.find(ws => ws.irn === entry.irn);
        if (!ws) {
            toAdd.push(entry);
        } else {
            toUpdate.push(entry);
        }
    });
    if (toAdd.length > 0) {
        await cds.tx(req).run(INSERT.into(db_namespace + 'Workspace').entries(toAdd));
    }
    if (toUpdate.length > 0) {
        for (var i = 0; i < toUpdate.length; i++) {
            await cds.tx(req).run(UPDATE.entity(db_namespace + 'Workspace').with(toUpdate[i]).where({ irn: toUpdate[i].irn }));
        }
    }

    // Deleted workspaces
    const toDelete = [];
    current.forEach(entry => {
        const ws = workspaces.find(ws => ws.irn === entry.irn);
        if (!ws) {
            toDelete.push(entry);
        }
    });
    if (toDelete.length > 0) {
        const entries = [];
        toDelete.forEach(entry => {
            entries.push(entry.irn);
        });
        let workplaces = await cds.tx(req).run(SELECT.from(db_namespace + 'Workplace').columns(['irn']).where({ space_irn: { 'IN': entries } }));
        workplaces = (workplaces.length === undefined) ? [workplaces] : workplaces;
        const places = [];
        workplaces.forEach(entry => {
            places.push(entry.irn);
        });
        // Delete bookings
        await cds.tx(req).run(DELETE.from(db_namespace + 'Booking').where({ place_irn: { 'IN': places } }));
        // Delete workplaces
        await cds.tx(req).run(DELETE.from(db_namespace + 'Workplace').where({ space_irn: { 'IN': entries } }));
        // Delete workspaces
        await cds.tx(req).run(DELETE.from(db_namespace + 'Workspace').where({ irn: { 'IN': entries } }));
    }
}

// Do the appropriate updates on workplaces
async function refreshWorkplaces(workplaces, space_irn, req) {
    // Get all current workplaces
    let current = await cds.tx(req).run(SELECT.from(db_namespace + 'Workplace').columns(['irn']).where({ space_irn: space_irn }));
    current = (current.length === undefined) ? [current] : current;

    // Added and/or updated workplaces
    const toAdd = [];
    const toUpdate = [];
    workplaces.forEach(entry => {
        const wp = current.find(wp => wp.irn === entry.irn);
        if (!wp) {
            toAdd.push(entry);
        } else {
            toUpdate.push(entry);
        }
    });
    if (toAdd.length > 0) {
        await cds.tx(req).run(INSERT.into(db_namespace + 'Workplace').entries(toAdd));
    }
    if (toUpdate.length > 0) {
        for (var i = 0; i < toUpdate.length; i++) {
            await cds.tx(req).run(UPDATE.entity(db_namespace + 'Workplace').with(toUpdate[i]).where({ irn: toUpdate[i].irn }));
        }
    }

    // Deleted workspaces
    const toDelete = [];
    current.forEach(entry => {
        const wp = workplaces.find(wp => wp.irn === entry.irn);
        if (!wp) {
            toDelete.push(entry);
        }
    });
    if (toDelete.length > 0) {
        const entries = [];
        toDelete.forEach(entry => {
            entries.push(entry.irn);
        });
        // Delete bookings
        await cds.tx(req).run(DELETE.from(db_namespace + 'Booking').where({ place_irn: { 'IN': entries } }));
        // Delete workplaces
        await cds.tx(req).run(DELETE.from(db_namespace + 'Workplace').where({ irn: { 'IN': entries } }));
    }
}

// Load Workspace information from external services
async function loadWorkspaceInfo(req) {
    const resp = await C4RE.get('/spaces');
    if (resp) {
        const content = resp.content;
        const workspaces = [];
        content.forEach(element => {
            const workspace = {
                irn: element.irn,
                shortName: element.shortName,
                longName: element.longName,
                type: 'Owned'
            }
            workspaces.push(workspace);
        });
        await refreshWorkspaces(workspaces, req);

        for (var i = 0; i < workspaces.length; i++) {
            const resp = await C4RE.get('/spaces/' + workspaces[i].irn + '/workplaces2');
            if (resp) {
                const content = resp.content;
                const workplaces = [];
                content.forEach(element => {
                    const workplace = {
                        irn: element.irn,
                        space_irn: element.spaceIrn,
                        space_name: workspaces[i].longName,
                        name: 'Workplace ' + element.name,
                    }
                    workplaces.push(workplace);
                });
                await refreshWorkplaces(workplaces, workspaces[i].irn, req);
            }
        }
    }
}

/*** HANDLERS ***/

// Update the DB at first read operation 
async function getData(req) {
    try {
        if (firstRead) {
            // Load external Workspace info into DB
            await loadWorkspaceInfo(req);

            // Reset control flag
            firstRead = false;
        }
        return req;
    } catch (err) {
        req.error(err.code, err.message);
    }
}

// Create CRUD controls for booking
function createBookingCRUD(req) {
    try {
        req.data.deletable = req.data.userId === req.user.id;
        req.data.updateHidden = !req.data.deletable;
        return req;
    } catch (err) {
        req.error(err.code, err.message);
    }
}

// Create CRUD controls for booking
async function updateBookingCRUD(data, req) {
    try {
        if (data) {
            if (data.length != undefined) {
                for (var i = 0; i < data.length; i++) {
                    const booking = data[i];
                    if (booking.userId === undefined) {
                        const bk = await cds.tx(req).run(SELECT.one.from(db_namespace + 'Booking', booking.ID).columns(['userId']));
                        booking.userId = (bk) ? bk.userId : null;
                    }
                    booking.deletable = (booking.userId === req.user.id);
                    booking.updateHidden = !booking.deletable;
                }
                data.sort((a, b) => {
                    da = new Date(a.fromDateTime);
                    db = new Date(b.fromDateTime);
                    return da - db;
                });
            } else {
                if (data.userId === undefined) {
                    const bk = await cds.tx(req).run(SELECT.one.from(db_namespace + 'Booking', data.ID).columns(['userId']));
                    data.userId = (bk) ? bk.userId : null;
                }
                data.deletable = data.userId === req.user.id;
                data.updateHidden = !data.deletable;
            }
        }
    } catch (err) {
        req.error(err.code, err.message);
    }
}

// Set booking space, place and user
async function setBookingSpaceAndUser(req) {
    try {
        if (req.data.place_irn === undefined) {
            req.data.place_irn = req.params[0].irn;
        }
        const space = await cds.tx(req).run(SELECT.one.from(db_namespace + 'Workplace', { irn: req.data.place_irn }).columns(['space_irn']));
        req.data.space_irn = (space) ? space.space_irn : null;
        req.data.userId = req.user.id;
        return req;
    } catch (err) {
        req.error(err.code, err.message);
    }
}

// Validate booking data
async function validateBookingData(req) {
    try {
        const bookings = req.data.bookings;
        for (var i = 0; i < bookings.length; i++) {
            const booking = bookings[i];
            // Check from
            if (!booking.fromDateTime) {
                req.error(400, 'Valid from date & time must be provided.');
            } else {
                // Check
                if (!booking.toDateTime) {
                    req.error(400, 'Valid until date & time must be provided.');
                } else {
                    // End date & time must greater than start date
                    const startDate = new Date(booking.fromDateTime);
                    const endDate = new Date(booking.toDateTime);
                    if (startDate.getTime() >= endDate.getTime()) {
                        req.error(400, 'End date & time must be greater than start date & time.');
                    } else {
                        // Check booking conflict
                        const hasBooking = await cds.tx(req).run(SELECT.one.from(db_namespace + 'Booking').where({ ID: { '<>': booking.ID }, and: { place_irn: booking.place_irn, and: { fromDateTime: { between: booking.fromDateTime, and: booking.toDateTime }, or: { toDateTime: { between: booking.fromDateTime, and: booking.toDateTime } } } } }));
                        if (hasBooking) {
                            req.error(400, 'Booking conflicts with another booking in the same period.');
                        }
                    }
                }
            }
        }

        return req;
    } catch (err) {
        req.error(err.code, err.message);
    }
}

// refreshData function handler
async function refreshData(req) {
    try {
        // Load external Workspace info into DB
        await loadWorkspaceInfo(req);
    } catch (err) {
        req.error(err.code, err.message);
    }
    return true;
}

// Force filtering on external workspaces only
function filterExternal(req) {
    try {
        if (req.params.length === 0) {
            if (req.query.SELECT.where === null || req.query.SELECT.where === undefined) {
                req.query.SELECT["where"] = [{ ref: ['type'] }, '=', { val: 'External' }];
            } else {
                let hasType = false;
                for (var i = 0; i < req.query.SELECT.where.length; i++) {
                    if (req.query.SELECT.where[i].ref != null && req.query.SELECT.where[i].ref != undefined) {
                        if (req.query.SELECT.where[i].ref[0] === 'type') {
                            hasType = true;
                            break;
                        }
                    }
                }
                if (!hasType) {
                    req.query.SELECT.where.push('and');
                    req.query.SELECT.where.push({ ref: ['type'] });
                    req.query.SELECT.where.push('=');
                    req.query.SELECT.where.push({ val: 'External' });
                }
            }
        }

        return req;
    } catch (err) {
        req.error(err.code, err.message);
    }
}

// Set fixed type for workspace
async function setWorkspaceType(req) {
    try {
        req.data.irn = 'space(' + btoa(randomUUID()) + ')';
        req.data.type = 'External';
        return req;
    } catch (err) {
        req.error(err.code, err.message);
    }
}

// Set workspace name for the workplace
async function setWorkspaceName(req) {
    try {
        req.data.irn = 'workplace(' + btoa(randomUUID()) + ')';
        if (req.data.space_irn === undefined) {
            req.data.space_irn = req.params[0].irn;
        }
        const space = await cds.tx(req).run(SELECT.one.from(db_namespace + 'Workspace', { irn: req.data.space_irn }).columns(['longName']));
        req.data.space_name = (space) ? space.longName : null;
        return req;
    } catch (err) {
        req.error(err.code, err.message);
    }
}

// Make sure all child workplaces have their corresponding space name assigned
function setWorkspaceNames(req) {
    try {
        if (req.data) {
            const workspace = req.data;
            if (workspace.workPlaces && workspace.workPlaces.length != undefined) {
                const workplaces = workspace.workPlaces;
                workplaces.forEach(workplace => {
                    workplace.space_name = workspace.longName;
                });
            }
        }
        return req;
    } catch (err) {
        req.error(err.code, err.message);
    }
}

// Sort child workplaces by name in ascending order
function sortWorkplaces(data) {
    if (data && data.length != undefined) {
        data.sort((a, b) => {
            const na = a.name.toLowerCase();
            const nb = b.name.toLowerCase();

            if (na < nb) {
                return -1;
            }
            if (na > nb) {
                return 1;
            }

            return 0;
        });
    }
}

// Exported functions
module.exports = {
    getData,
    createBookingCRUD,
    updateBookingCRUD,
    setBookingSpaceAndUser,
    validateBookingData,
    refreshData,
    filterExternal,
    setWorkspaceType,
    setWorkspaceName,
    setWorkspaceNames,
    sortWorkplaces
}