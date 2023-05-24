const { filterExternal, setWorkspaceType, setWorkspaceName, setWorkspaceNames, sortWorkplaces } = require('./lib/handlers');

module.exports = cds.service.impl(async function () {
    /*** SERVICE ENTITIES ***/
    const {
        Workspace,
        Workplace
    } = this.entities;

    /*** SERVICE HANDLERS ***/
    this.before('READ', Workspace, filterExternal);
    this.before('NEW', Workspace, setWorkspaceType);
    this.before('SAVE', Workspace, setWorkspaceNames);
    this.before('NEW', Workplace, setWorkspaceName);
    this.after('READ', Workplace, sortWorkplaces);
});