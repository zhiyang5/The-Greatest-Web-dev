import { MigrationInterface, QueryRunner, Table } from 'typeorm';

export class UserTable1716972199792 implements MigrationInterface {

    public async up(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.createTable(
            new Table({
                name: 'users',
                columns: [
                    {
                        name: 'id',
                        type: 'uuid',
                        isPrimary: true,
                        isGenerated: true,
                        primaryKeyConstraintName: 'pk-users_uuid',
                    },
                    {
                        name: 'first_name',
                        type: 'varchar',
                    },
                    {
                        name: 'username',
                        type: 'text',
                    },
                    {
                        name: 'last_name',
                        type: 'varchar',
                    },
                    {
                        name: 'email',
                        type: 'varchar(320)',
                        isUnique: true,
                    },
                    {
                        name: 'password',
                        type: 'text',
                    },
                    {
                        name: 'phoneNum',
                        type: 'text',
                    },
                ],
            }),
        );
    }

    public async down(queryRunner: QueryRunner): Promise<void> {
        await queryRunner.dropTable('users');
    }

}
