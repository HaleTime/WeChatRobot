from sqlalchemy import create_engine
import os
from sqlalchemy.orm import sessionmaker
from db.models import Base


project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(project_root, 'db_data', 'wechat.db')


# 创建 SQLite 数据库引擎
engine = create_engine(f'sqlite:///{db_path}', echo=True)

# 创建数据库表（如果尚不存在）
Base.metadata.create_all(engine)

# 创建会话
Session = sessionmaker(bind=engine)
