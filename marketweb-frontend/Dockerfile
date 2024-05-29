FROM node
WORKDIR /marketweb-frontend
COPY . .
RUN npm ci
EXPOSE 5173
CMD ["npm", "run", "dev"]