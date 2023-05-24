const { getData, createBookingCRUD, updateBookingCRUD, setBookingSpaceAndUser, validateBookingData, refreshData } = require('./lib/handlers');

module.exports = cds.service.impl(async function () {
    /*** SERVICE ENTITIES ***/
    const {
        Workspace,
        Workplace,
        Booking
    } = this.entities;

    /*** SERVICE HANDLERS ***/
    this.before('READ', Workspace, getData);
    this.before('READ', Workplace, getData);
    this.before('SAVE', Workplace, validateBookingData);
    this.before('READ', Booking, getData);
    this.before('CREATE', Booking, createBookingCRUD);
    this.before('NEW', Booking, setBookingSpaceAndUser);
    this.after('READ', Booking, updateBookingCRUD);
    this.on('refreshData', refreshData);
});