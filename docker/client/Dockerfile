FROM mcr.microsoft.com/dotnet/core/sdk:3.0-alpine AS runtime
RUN apk update \
        && apk upgrade \
        && apk add --no-cache bash \
        && rm -rf /var/cache/apk/*

WORKDIR /app
COPY ./docker/wait-for-it.sh ./
RUN chmod +x ./wait-for-it.sh

COPY *.sln .
COPY ./src/DeepCard.Client.Client ./src/DeepCard.Client.Client
COPY ./src/DeepCard.Client.SDK ./src/DeepCard.Client.SDK
COPY ./src/DeepCard.Client.Server ./src/DeepCard.Client.Server
COPY ./src/DeepCard.Server ./src/DeepCard.Server

RUN dotnet restore

RUN cd ./src/DeepCard.Client.Server && dotnet build

EXPOSE 8000/tcp

ENTRYPOINT ["dotnet", "run", "-p", "./src/DeepCard.Client.Server"]