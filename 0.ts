import { Connection } from 'mysql2';

class UserService {
    private db: Connection;

    constructor(db: Connection) {
        this.db = db;
    }

    // 这个方法存在 SQL 注入漏洞
    async getUserData(userId: string) {
        // 危险: 直接拼接用户输入到 SQL 查询中
        const query = `SELECT * FROM users WHERE id = '${userId}'`;

        try {
            // 执行不安全的查询
            const result = await this.db.query(query);
            return result;
        } catch (error) {
            console.error('Error fetching user:', error);
            throw error;
        }
    }

    // 这个方法也存在潜在的命令注入漏洞
    async executeCommand(command: string) {
        const { exec } = require('child_process');

        // 危险: 直接执行用户提供的命令
        return new Promise((resolve, reject) => {
            exec(command, (error: Error, stdout: string, stderr: string) => {
                if (error) {
                    reject(error);
                    return;
                }
                resolve(stdout);
            });
        });
    }
}

// 使用示例
async function main() {
    const db = {} as Connection; // 示例中省略实际的数据库连接
    const userService = new UserService(db);

    // 这里可能导致 SQL 注入
    const userData = await userService.getUserData("1' OR '1'='1");

    // 这里可能导致命令注入
    const result = await userService.executeCommand("ls -la");
}

export { UserService };
