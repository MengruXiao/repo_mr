# todo:   from S3 to 本地
aws s3 cp --recursive s3://myBucket/dir localdir

aws s3 cp --recursive s3://myBucket/dir localdir 是一个 AWS CLI 命令，用于从 AWS S3 存储桶中复制文件到本地目录。这条命令的具体作用如下：

aws: 调用 AWS 命令行界面 (CLI)。
s3: 指定要使用的 AWS 服务是 S3（Simple Storage Service）。
cp: 表示“copy”，即复制操作。
--recursive: 这是一个选项，表示要递归地复制 S3 存储桶中的目录及其所有子目录和文件。
s3://myBucket/dir: 这是 S3 存储桶中的源路径。s3:// 是 S3 URI 的前缀，myBucket 是存储桶的名称，dir 是存储桶中的一个目录。
localdir: 这是本地文件系统中的目标路径，即你想要将文件复制到的位置。
综合起来，aws s3 cp --recursive s3://myBucket/dir localdir 命令将从名为 myBucket 的 S3 存储桶中的 dir 目录（及其所有子目录和文件）递归地复制到本地文件系统中的 localdir 目录。

在运行此命令之前，你需要确保已经安装了 AWS CLI，并且已经通过 aws configure 命令配置了你的 AWS 凭证（访问密钥和密钥ID）以及默认的区域设置。此外，确保你的本地机器有访问 S3 存储桶的权限，并且 localdir 目录已经存在或者你愿意创建它。

# todo:   from 本地 to S3

aws s3 cp --recursive  localdir s3://myBucket/dir

aws s3 cp --recursive localdir s3://myBucket/dir 是一个 AWS CLI 命令，用于将本地目录及其内容递归地上传到 AWS S3 存储桶中的指定目录。这条命令的详细解释如下：

aws: 调用 AWS 命令行界面 (CLI)。
s3: 指定要使用的 AWS 服务是 S3（Simple Storage Service）。
cp: 表示“copy”，即复制操作。
--recursive: 这是一个选项，表示要递归地复制本地目录中的所有子目录和文件。
localdir: 这是本地文件系统中的源路径，即你想要上传的目录。
s3://myBucket/dir: 这是 S3 存储桶中的目标路径。s3:// 是 S3 URI 的前缀，myBucket 是存储桶的名称，dir 是存储桶中的一个目录，文件将被上传到这个目录下。
综合起来，aws s3 cp --recursive localdir s3://myBucket/dir 命令将递归地从本地文件系统中的 localdir 目录复制所有文件和子目录到名为 myBucket 的 S3 存储桶中的 dir 目录。

在运行此命令之前，你需要确保已经安装了 AWS CLI，并且已经通过 aws configure 命令配置了你的 AWS 凭证（访问密钥和密钥ID）以及默认的区域设置。此外，确保你的本地机器有权限上传文件到 S3 存储桶，并且 S3 存储桶和目录（myBucket 和 dir）已经存在。如果 dir 目录在 S3 存储桶中不存在，AWS CLI 将尝试创建它。


