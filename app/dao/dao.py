from app.config import Config
from . import dao_sql
from . import dao_orm_models

if Config.DAO_SQL:
    SpeciesDAO = dao_sql.SpeciesDaoSql()
    AnimalCenterDAO = dao_sql.AnimalCentersDaoSql()
    AccessRequestDAO = dao_sql.AccessRequestDaoSql()
    AnimalDAO = dao_sql.AnimalsDaoSql()
else:
    SpeciesDAO = dao_orm_models.SpeciesORM()
    AnimalCenterDAO = dao_orm_models.AnimalCenterORM()
    AccessRequestDAO = dao_orm_models.AccessRequestORM()
    AnimalDAO = dao_orm_models.AnimalORM()
