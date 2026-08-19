# Data provenance

The study used free public Binance market data for BTC, ETH, SOL, and the
external momentum universe, plus Yahoo Finance `GC=F` daily observations for
gold. Raw inputs are not redistributed because they are larger, provider-owned,
and re-downloadable only subject to current upstream terms.

The public evidence artifact is `data/processed/returns_matrix.csv`. It contains
four cost-adjusted BTC-hourly strategy return series aligned by UTC timestamp.
Its SHA-256 and byte count are declared in both manifests. This identity, not a
future market-data download, is the basis of the frozen statistical release.

Any new raw-data ingestion should record provider, endpoint, symbols, interval,
UTC conversion, inclusive time range, download timestamp, adjustment policy,
and SHA-256 before a processed artifact is promoted.
