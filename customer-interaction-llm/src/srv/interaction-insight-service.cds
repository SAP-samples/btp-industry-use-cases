using {xxx.cust.int.llm as db} from '../db/customer-interaction-db';
using { AdminService } from './admin-service';

extend service AdminService {
  @readonly
  entity InteractionInsight as projection on db.CustomerInteraction {
    *,
    substring(createdAt,1,4) as riskyear:String,
    cast (substring(createdAt,1,10) as Date) as createdAt
  };
}

extend AdminService.InteractionInsight with @cds.redirection.target;