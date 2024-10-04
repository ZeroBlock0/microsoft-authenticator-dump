# microsoft-authenticator-pump

把TOTP导出来

1. 找到数据
   Microsoft Authenticator 中的2FA密钥数据存储路径为 /data/data/com.azure.authenticator/databases/PhoneFactor。
2. PhoneFactor 文件本身是Sqlite数据库文件，所以复制文件时候需要复制PhoneFactor PhoneFactor-shm PhoneFactor-wal 这三个文件（如果有），可以通过Sqlite数据库操作软件来查看具体的数据信息。想要的数据就在 accounts 表中。
3. 使用pump.py提取
4. account_type为1的是微软本身的账户，为0的是手动添加的第三方账户。
5. 导入数据
   拿到数据以后我们可以导入到自己想要使用的任意软件了，可以手动输入secret_key，也可以直接将上面otpauth://开头的url直接生成二维码进行扫码导入。




Exporting TOTP

1. Locate the dataThe storage path for the 2FA key data in Microsoft Authenticator is /data/data/com.azure.authenticator/databases/PhoneFactor.
2. The PhoneFactor file itself is an SQLite database file, so when copying, you need to copy the PhoneFactor, PhoneFactor-shm, and PhoneFactor-wal files (if available). You can use an SQLite database management tool to view the specific data information. The desired data can be found in the accounts table.
3. Extracting with pump.py
4. An account_type of 1 indicates a Microsoft account, while 0 indicates a manually added third-party account.
5. Importing the data
   Once you have the data, you can import it into any software you want to use. You can manually enter the secret_key or directly generate a QR code from the otpauth:// URL to scan and import.
