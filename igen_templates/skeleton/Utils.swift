func after(interval: TimeInterval, completion: (() -> Void)?) {
    DispatchQueue.main.asyncAfter(deadline: .now() + interval) {
        completion?()
    }
}

func validate<T>(object: Driver<T>,
                 trigger: Driver<Void>,
                 validator: @escaping (T) -> ValidationResult) -> Driver<ValidationResult> {
    return Driver.combineLatest(object, trigger)
        .map { $0.0 }
        .map { validator($0) }
        .startWith(.valid)
}
