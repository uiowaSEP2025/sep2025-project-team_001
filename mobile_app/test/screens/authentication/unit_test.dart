import 'package:flutter_test/flutter_test.dart';
import 'package:dio/dio.dart';
import 'package:mobile_app/authentication/authentication_screen.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

@GenerateMocks([Dio])
import 'unit_tests.mocks.dart';  // Auto-generated file

void main() {
  group('AuthenticationPage Unit Tests', () {
    late MockDio mockDio;
    late AuthenticationPage authenticationPage;

    setUp(() {
      mockDio = MockDio();
      authenticationPage = const AuthenticationPage();
    });

    test('Dio login request should return success', () async {
      when(mockDio.post(
        any,
        data: anyNamed('data'),
        options: anyNamed('options'),
      )).thenAnswer((_) async => Response(
            data: {'message': 'Success'},
            statusCode: 200,
            requestOptions: RequestOptions(path: ''),
          ));

      final response = await mockDio.post('http://localhost:8000/auth/login/',
          data: {"username": "test@gmail.com", "password": "password123"},
          options: Options(headers: {"Content-Type": "application/json"}));

      expect(response.statusCode, 200);
      expect(response.data['message'], 'Success');
    });

    test('Dio login request should return error', () async {
      when(mockDio.post(
        any,
        data: anyNamed('data'),
        options: anyNamed('options'),
      )).thenThrow(DioError(
        requestOptions: RequestOptions(path: ''),
        response: Response(
            data: {'error': 'Invalid credentials'},
            statusCode: 401,
            requestOptions: RequestOptions(path: '')),
      ));

      try {
        await mockDio.post('http://localhost:8000/auth/login/',
            data: {"username": "wrong@gmail.com", "password": "wrongpassword"},
            options: Options(headers: {"Content-Type": "application/json"}));
      } catch (error) {
        expect(error, isInstanceOf<DioError>());
      }
    });
  });
}
