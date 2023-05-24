namespace fdt_app.db;

using {HCM} from '../srv/external/HCM';
using {S4} from '../srv/external/S4';

@readonly
entity Employee as projection on HCM.User {
    userId,
    defaultFullName,
    department,
    division,
    email,
    firstName,
    lastName,
    title,
    history : Association to many DriveHistory on history.driver = $self
};

@readonly
entity Vehicle  as projection on S4.YY1_Vehicles1710 {
    key CompanyCode               as company,
    key MasterFixedAsset          as code,
    key FixedAsset                as asset,
        AssetClassName            as className,
        FixedAssetDescription     as name,
        VehicleLicensePlateNumber as licensePlate
};

@readonly
entity VehicleDrive  as projection on S4.YY1_Vehicles1710 {
    key MasterFixedAsset          as code,
        FixedAssetDescription     as name,
        VehicleLicensePlateNumber as licensePlate
};

entity DriveHistory {
    key driver                          : Association to one Employee;
    key startDateTime                   : DateTime;
    key endDateTime                     : DateTime;
        vehicle                         : Association to one VehicleDrive;
        distance                        : Integer;
        fuelConsumption                 : Decimal;
        maxRPM                          : Integer;
        maxSpeed                        : Integer;
        nbHarshBraking                  : Integer;
        nbHarshCornering                : Integer;
        nbRapidAcceleration             : Integer;
        nbTailGating                    : Integer;
        nbInfoTainmentUsageWhileDriving : Integer;
}
