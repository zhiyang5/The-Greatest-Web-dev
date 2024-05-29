import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import typeorm from './config/typeorm';
import { ConfigModule, ConfigService } from '@nestjs/config';
import "reflect-metadata"
@Module({
    imports: [
        // config for migrations from https://dev.to/amirfakour/using-typeorm-migration-in-nestjs-with-postgres-database-3c75
        ConfigModule.forRoot({
            isGlobal: true,
            load: [typeorm],
        }),
        TypeOrmModule.forRootAsync({
            inject: [ConfigService],
            useFactory: async (configService: ConfigService) =>
                configService.get('typeorm'),
        }),
    ],
    controllers: [],
    providers: [],
})
export class AppModule {}