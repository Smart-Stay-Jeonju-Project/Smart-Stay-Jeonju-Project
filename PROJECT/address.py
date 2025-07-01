# 주소 정보를 좌표 정보로 변환 수정필요함

# import pandas as pd
# import googlemaps

# googlemaps_key = "AIzaSyDg8UOceSAXDR2NnMikougMamOyAxbdRac"
# gmaps = googlemaps.Client(key=googlemaps_key)

# df = pd.read_csv('./DATA/list/숙소상세정보(중복제거).csv')	# 데이터 읽기 입니다(사람마다 다름)

# col = df['주소']			    # 데이터 읽기 입니다(사람마다 다름)

# # 저는 이렇게 3 종류의 데이터를 담으려 합니다.
# address = []
# latitude = []
# longitude = []

# for add in col:
#     response = gmaps.geocode(add) 	# response의 데이터 타입은 list입니다.
#     if response:			        # response가 유효할 때만
#         if add not in address:    	# 주소 겹치는 건 다시 할 필요가 없으니
#             geo_location = response[0].get('geometry')

#             lat = geo_location['location']['lat']
#             lng = geo_location['location']['lng']

#             print(add, lat, lng)    
#             address.append(add)
#             latitude.append(lat)
#             longitude.append(lng)

# data = {'address': address, 'latitude': latitude, 'longitude': longitude}

# data_df = pd.DataFrame(data)

# # 이 파일은 csv(,로 구분)이고 한글 깨지면 안되고 output.csv로 저장해주세요 라는 뜻입니다
# data_df.to_csv(r'YOUR PATH\output.csv', sep=',', encoding="utf-8-sig")