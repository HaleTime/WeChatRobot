from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# 创建 SQLite 数据库引擎
engine = create_engine('sqlite:///db_data/wechat.db', echo=True)

# 创建数据库表（如果尚不存在）
Base.metadata.create_all(engine)

# 创建会话
Session = sessionmaker(bind=engine)