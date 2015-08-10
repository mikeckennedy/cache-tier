import cache_tier


def main():
    base_url = "http://localhost:5000/"
    file = '016-Netflix-roy-rapaport.mp3'

    while True:
        input("Enter to simulate request")

        cache = cache_tier.CacheTierClient(
            base_url,
            local_cache_time=20,
            log_enabled=True)

        if cache.verify_file(file):
            print("File validated, would download at:")
            print(cache.build_download_url(file))
        else:
            print("File NOT validated")
        print()


if __name__ == "__main__":
    main()
