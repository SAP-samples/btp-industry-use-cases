using {xxx.cust.int.llm as db} from '../db/customer-interaction-db';
using {AdminService} from './admin-service';

extend service AdminService {
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

extend AdminService.InteractionInsight with @cds.redirection.target;
extend AdminService.InboundCustomerMessage with @cds.redirection.target;
