using {xxx.cust.int.llm as db} from '../db/customer-interaction-db';
using {TicketingService} from './ticketing-service';

extend service TicketingService {
  @readonly
  entity InteractionInsight          as projection on db.CustomerInteraction {
    *,
    category.name as catname @(title: '{i18n>catname}'),
    priority.name as priorname @(title: '{i18n>priorname}'),
    status.name   as statname @(title: '{i18n>statname}'),
    substring(
      createdAt, 1, 4
    )             as riskyear : Integer,
    cast(
      substring(
        createdAt, 1, 10
      ) as                      Date
    )             as createdAt
  };

}

extend TicketingService.InteractionInsight with @cds.redirection.target;
extend TicketingService.InboundCustomerMessage with @cds.redirection.target;
