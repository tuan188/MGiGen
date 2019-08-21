protocol {{ name }}UseCaseType {
    {% if paging %}
    func get{{ model_name }}List(page: Int) -> Observable<PagingInfo<{{ model_name }}>>
    {% else %}
    func get{{ model_name }}List() -> Observable<[{{ model_name }}]>
    {% endif %}
}

struct {{ name }}UseCase: {{ name }}UseCaseType {
    {% if paging %}
    func get{{ model_name }}List(page: Int) -> Observable<PagingInfo<{{ model_name }}>> {
        return Observable.empty()
    }
    {% else %}
    func get{{ model_name }}List() -> Observable<[{{ model_name }}]> {
        return Observable.empty()
    }
    {% endif %}
}
