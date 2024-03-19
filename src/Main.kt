fun decimalTo26Base(decimal: Int): String {
    var num = decimal
    val sb = StringBuilder()

    if (num > 18277) {
        throw Exception("cannot over the biggest of ZZZ")
    }

    while (num >= 0) {
        val remainder = num % 26
        sb.insert(0, 'A' + remainder)
        num /= 26
        num--
    }

    return sb.toString()
}

fun transformNumbersToExcelColumnNames(number: Int, length: Int): List<String> {
    val list = mutableListOf<String>()
    var num = number
    repeat(length) {
        list.add(decimalTo26Base(num - 1))
        num++
    }
    return list
}

fun main(args: Array<String>) {
    println(transformNumbersToExcelColumnNames(1, 1))
    println(transformNumbersToExcelColumnNames(1, 2))
    println(transformNumbersToExcelColumnNames(26, 3))
    println(transformNumbersToExcelColumnNames(18278, 2))
}