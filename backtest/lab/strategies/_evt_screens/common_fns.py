def trade(i, j, side, H, stop=None, hedge=False):
    """enter at o[i+1]; exit at o[i+1+H] or stop (intrabar, pessimistic at stop or open gap)."""
    a = i + 1
    if a >= T or not np.isfinite(o[a, j]):
        return None
    e = o[a, j]
    b = min(a + H, T - 1)
    ex = None; k_exit = b
    for k in range(a, b):
        if not np.isfinite(h[k, j]):
            ex = c[k - 1, j] if k > a and np.isfinite(c[k - 1, j]) else e; k_exit = k; break
        if stop is not None:
            sp = e * (1 + stop) if side < 0 else e * (1 - stop)
            if side < 0 and h[k, j] >= sp:
                ex = max(sp, o[k, j]); k_exit = k + 1; break
            if side > 0 and l[k, j] <= sp:
                ex = min(sp, o[k, j]); k_exit = k + 1; break
    if ex is None:
        ex = o[b, j] if np.isfinite(o[b, j]) else c[b - 1, j]
    r = side * (ex / e - 1)
    fund = -side * np.nansum(f[a:k_exit, j])  # short receives positive funding
    rb = 0.0
    if hedge:
        eb = o[a, bj]; xb = o[min(k_exit, T - 1), bj]
        rb = -side * (xb / eb - 1)            # opposite BTC leg, beta 1
    return dict(i=i, j=j, r=r, fund=fund, rb=rb, net=r + fund - COST, neth=r + rb + fund - 2 * COST,
                stopped=k_exit < b, days=(k_exit - a) / BPD)

def summarize(name, ev):
    if not ev:
        print(name, "no events"); return
    d = pd.DataFrame(ev)
    d["t"] = pd.to_datetime(p.t[d.i], unit="s")
    yr = d.groupby(d.t.dt.year).net.agg(["size", "mean"]).round(4).to_dict("index")
    print(f"{name:42s} n={len(d):4d} gross={d.r.mean():+.4f} fund={d.fund.mean():+.4f} net={d.net.mean():+.4f} "
          f"med={d.net.median():+.4f} hit={(d.net>0).mean():.2f} worst={d.net.min():+.3f} hedged={d.neth.mean():+.4f} "
          f"stop%={d.stopped.mean():.2f} t={d.net.mean()/d.net.std()*np.sqrt(len(d)):.2f} yr={yr}")

