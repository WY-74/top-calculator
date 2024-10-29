from typing import List


class E245Dmips:
    """
    用于吉利E245算力统计
    N dmips = cpus% / 6 / 100 * 80
    在均值计算过程中，排除最大值和最小值；所有数据均精确到两位小数
    """

    def _get_effective_cpus(self, cpus: List[float], accept_zero: bool = True):
        if not accept_zero:
            cpus = [x for x in cpus if x != 0]

        _max = max(cpus)
        _min = min(cpus)

        cpus = [x for x in cpus if x != _max and x != _min]
        return _max, _min, cpus

    def _get_dmips(self, cpus: List[float]):
        return [round(cpu / 8 / 100 * 60, 2) for cpu in cpus]

    def run(self, groups):
        results = ""

        for k in groups.keys():
            results += f"##### {k} [{groups[k]["arg"]}][{len(groups[k]["data"])}] #####\n"

            cpus = [float(i[7]) for i in groups[k]["data"]]
            _max, _min, cpus = self._get_effective_cpus(cpus)
            _avg = round(sum(cpus) / len(cpus), 2)

            dmax, dmin, davg = self._get_dmips([_max, _min, _avg])
            results += f"\t\tmin: {_min}({dmin})\n\t\tmax: {_max}({dmax})\n\t\tavg: {_avg}({davg})\n\n"

        print(results)


class DFcpus:
    """
    东风性能统计
    展示完整数据列表，cpu最大值和平均值
    在均值计算过程中，排除最大值和最小值；所有数据均精确到两位小数
    """

    def _get_effective_cpus(self, cpus: List[float], accept_zero: bool = True):
        if not accept_zero:
            cpus = [x for x in cpus if x != 0]

        _max = max(cpus)
        _min = min(cpus)

        cpus = [x for x in cpus if x != _max and x != _min]
        cpus.sort()
        return _max, cpus

    def run(self, groups):
        results = ""

        for k in groups.keys():
            results += f"##### {k} [{groups[k]['arg']}][{len(groups[k]['data'])}] #####\n"

            cpus = [float(i[7]) for i in groups[k]["data"]]
            _max, cpus = self._get_effective_cpus(cpus)
            _avg = round(sum(cpus) / len(cpus), 2)

            results += f"{cpus}\n\t\tmax: {_max}\n\t\tavg: {_avg}\n\n"

        print(results)


class Threads:
    """
    线程cpu统计
    展示完整数据列表，线程cpu最大值和平均值
    在均值计算过程中，不去掉最大值和最小值；所有数据均精确到两位小数
    """

    def _get_effective_cpus(self, cpus: List[float], accept_zero: bool = True):
        if not accept_zero:
            cpus = [x for x in cpus if x != 0]

        _max = max(cpus)
        _min = min(cpus)
        if _max == 0 and _min == 0:
            return None, None, None

        return _max, _min, cpus

    def _get_dmips(self, cpus: List[float]):
        return [round(cpu / 8 / 100 * 60, 2) for cpu in cpus]

    def run(self, groups):
        results = ""

        for k in groups.keys():
            cpus = [float(i[7]) for i in groups[k]["data"]]
            _max, _min, cpus = self._get_effective_cpus(cpus)
            if cpus is None:
                continue
            _avg = round(sum(cpus) / len(cpus), 2)
            dmax, dmin, davg = self._get_dmips([_max, _min, _avg])

            results += f"##### {k} [{groups[k]["arg"]}][{len(groups[k]["data"])}] #####\n"
            results += f"\t\tmin: {_min}({dmin})\n\t\tmax: {_max}({dmax})\n\t\tavg: {_avg}({davg})\n\n"

        print(results)