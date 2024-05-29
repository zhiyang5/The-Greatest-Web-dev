import { registerAs } from '@nestjs/config';
import { DataSource, DataSourceOptions } from 'typeorm';

// base config from https://dev.to/amirfakour/using-typeorm-migration-in-nestjs-with-postgres-database-3c75
const db_config = {
    type: 'postgres',

    // these will need to be env vars in the cloud
    host: 'db', // this is the docker container on the db-net network
    port: 5432,
    username: 'root',
    password: 'root',
    // end of env vars

    database: 'marketweb',
    entities: ['dist/resources/**/*.entity{.ts,.js}'],
    migrations: ['dist/migrations/*{.ts,.js}'],
    autoloadEntities: true,
    synchronize: false,
    migrationsTransactionMode: 'each',
    migrationsTableName: 'migrations',
};

export default registerAs('typeorm', () => db_config);
export const connectionSource = new DataSource(db_config as DataSourceOptions);