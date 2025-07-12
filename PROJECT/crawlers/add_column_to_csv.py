import os
import pandas as pd

def load_csv_file(file_path: str) -> pd.DataFrame :
    """CSV 파일을 읽어 DataFrame으로 반환"""
    return pd.read_csv(file_path, encoding='utf-8-sig')

def add_column(df, column_name: str, value) -> pd.DataFrame :
    """지정된 컬럼명을 추가하고 값을 일괄 입력"""
    df[column_name] = value
    return df

def save_df(df: pd.DataFrame, save_path: str) :
    """DataFrame을 지정된 경로로 저장"""
    df.to_csv(save_path, encoding='utf-8-sig', index=False, header=True)
    return

def main() :
    target_dir = 'DATA/RAW/REVIEWS/YEOGI/'
    input_filename = '1_14_18_366_y_reviews.csv'
    output_filename = 'source_reviews.csv'

    input_path = os.path.join(target_dir, input_filename)
    output_path = os.path.join(target_dir, output_filename)

    df = load_csv_file(input_path)
    df = add_column(df, column_name='source', value='y')
    save_df(df, output_path)

if __name__ == '__main__' :
    main()