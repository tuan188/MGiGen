protocol {{ name }}UseCaseType {
    func get{{ model_name }}List(page: Int) -> Observable<PagingInfo<{{ model_name }}>>
}

struct {{ name }}UseCase: {{ name }}UseCaseType {
    func get{{ model_name }}List(page: Int) -> Observable<PagingInfo<{{ model_name }}>> {
        return Observable.empty()
    }
}
