# class SourceNodeType(str, Enum):
from enum import Enum
from src.util import util
from pydantic import BaseModel, Field


SourceNodeType = Enum('SourceNodeType', util.get_node_types_from_directory())

class SourceHandle(str, Enum):
    source = "source"
    true = "true"
    false = "false"
    condition_1 = "1"
    condition_2 = "2"
    condition_3 = "3"
    condition_4 = "4"
    condition_5 = "5"
    condition_6 = "6"
    condition_7 = "7"
    condition_8 = "8"
    condition_9 = "9"
    condition_10 = "10"


class Edge(BaseModel):
    source_node_id: str = Field(..., description="自分自身のノードID IDは source_node_id+sourceHandle+target_node_id+target_node_type で一意になるように設定、全体を24文字にする")
    source_node_type:SourceNodeType = Field(..., description="自分自身のノードタイプ")
    target_node_id: str = Field(..., description="出力先のノードID")
    target_node_type: SourceNodeType = Field(..., description="出力先のノードタイプ")
    sourceHandle: SourceHandle = Field(..., description="source_node_typeがif-elseの場合は true もしくは false を指定、source_node_typeがquestion-classifierの時は分類用のクラスを数字で表記して数字を(1-10)を指定、それ以外はsourceを指定")
    description: str= Field(..., description="自分自身が何を行うのか説明")
    isInIteration: bool = Field(..., description="自分自身がイテレーションの中にあるかどうか")
    iteration_id: str = Field(..., description="自分自身がイテレーションの中にある場合はイテレーションのIDを指定 ない場合は Noneを指定")