module.exports = cds.service.impl(async function () {
    /*** SERVICE ENTITIES ***/
    const {
        Employee,
        DriveHistory
    } = this.entities;

    /*** SERVICE HANDLERS ***/
    this.before('READ', Employee, async req => {
        try {
            if (req.params.length === 0) {
                if (req.query.SELECT.where === null || req.query.SELECT.where === undefined) {
                    req.query.SELECT["where"] = [{ ref: ['department'] }, '=', { val: 'Fleet Drivers (50007728)' }];
                } else {
                    let hasDept = false;
                    for (var i = 0; i < req.query.SELECT.where.length; i++) {
                        if (req.query.SELECT.where[i].ref != null && req.query.SELECT.where[i].ref != undefined) {
                            if (req.query.SELECT.where[i].ref[0] === 'department') {
                                hasDept = true;
                                break;
                            }
                        }
                    }
                    if (!hasDept) {
                        req.query.SELECT.where.push('and');
                        req.query.SELECT.where.push({ ref: ['department'] });
                        req.query.SELECT.where.push('=');
                        req.query.SELECT.where.push({ val: 'Fleet Drivers (50007728)' });
                    }
                }
            }

            return req;
        } catch (err) {
            req.error(err.code, err.message);
        }
    });

    this.before('READ', DriveHistory, async req => {
        try {
            if (req.params.length > 1) {
                if (req.params[1].driver_userId != undefined) {
                    req.query.SELECT.from.ref.splice(0, 1);
                    req.query.SELECT.from.ref[0].id = 'FDTAppService.DriveHistory';
                }
            }
            return req;
        } catch (err) {
            req.error(err.code, err.message);
        }
    });
});