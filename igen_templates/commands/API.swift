// MARK: - {{ name }}
extension API {
    func {{ var_name }}(_ input: {{ name }}Input) -> Observable<{{ name }}Output> {
        return request(input)
    }

    final class {{ name }}Input: APIInput {
        init() {
            super.init(urlString: API.Urls.{{ var_name }},
                       parameters: nil,
                       requestType: .get,
                       requireAccessToken: true)
        }
    }

    final class {{ name }}Output: APIOutput {
        override func mapping(map: Map) {
            super.mapping(map: map)
        }
    }
}
